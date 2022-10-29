#this whole file can be changed depending on what we need to do with the data and how we want our OOP instances to appear.

# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user, comment
from flask import flash

# Hero = user.User
db = "dojo_wall_schema"

class Post:

    def __init__( self, data ):
        self.id = data['id']
        self.user_id = data['user_id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None
        self.comments = []
    # Now we use class methods to query our database

    @classmethod
    def get_all_posts_with_user(cls):
        # adjust the "FROM" target to be the required table
        query = "SELECT * FROM posts JOIN users ON posts.user_id = users.id ORDER BY posts.created_at DESC;"
        # make sure to call the connectToMySQL function with the DB schema you are targeting.
        results = connectToMySQL(db).query_db(query)
        all_posts = []
        for post in results:
            one_post = cls(post)
            one_post_user_info = {
                'id': post['users.id'],
                'first_name': post['first_name'],
                'last_name': post['last_name'],
                'email': post['email'],
                'password': post['password'],
                'created_at': post['users.created_at'],
                'updated_at': post['users.updated_at']
            }
            one_user = user.User(one_post_user_info)
            one_post.user = one_user
            all_posts.append( one_post )
            one_post.comments = comment.Comment.get_all_comments_with_user({'post_id':one_post.id})
        return all_posts

    @staticmethod
    def validate_post(content):
        is_valid = True
        if len(content['new_post']) <= 0:
            flash('Post body can not be blank', 'pos')
            is_valid = False
        return is_valid

    @classmethod
    def add_post(cls, data):
        query = "INSERT INTO posts (user_id, content) VALUES (%(user_id)s, %(new_post)s);"
        return connectToMySQL(db).query_db(query,data)
    
    @classmethod
    def delete_post(cls, data):
        query = "DELETE FROM posts WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)