#this whole file can be changed depending on what we need to do with the data and how we want our OOP instances to appear.

# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

db = "dojo_wall_schema"


class Comment:

    def __init__( self, data ):
        self.id = data['id']
        self.post_id = data['post_id']
        self.user_id = data['user_id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None
        self.post_list = []
    # Now we use class methods to query our database

    @classmethod
    def get_all_comments_with_user(cls,data):
        query = 'SELECT * FROM comments JOIN users ON comments.user_id = users.id WHERE comments.post_id = %(post_id)s ORDER BY comments.created_at DESC;'
        results = connectToMySQL(db).query_db(query,data)
        all_comments = []
        for row in results:
            one_comment = cls(row)
            one_comment_user = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            one_comment.user = user.User(one_comment_user)
            all_comments.append(one_comment)
        return all_comments

            
    @classmethod
    def add_comment(cls, data):
        query = "INSERT INTO comments (post_id, user_id, content) VALUES (%(post_id)s, %(user_id)s, %(new_comment)s);"
        return connectToMySQL(db).query_db(query,data)

    @staticmethod
    def validate_comment(content):
        is_valid = True
        if len(content['new_comment']) <= 0:
            flash('Comment body can not be blank', f'{content["post_id"]}')
            is_valid = False
        return is_valid