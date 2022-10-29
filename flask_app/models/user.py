#this whole file can be changed depending on what we need to do with the data and how we want our OOP instances to appear.

# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import post


db = "dojo_wall_schema"

class User:

    def __init__( self, data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.posts = []
    # Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        # adjust the "FROM" target to be the required table
        query = "SELECT * FROM users;"
        # make sure to call the connectToMySQL function with the DB schema you are targeting.
        results = connectToMySQL(db).query_db(query)
        users = []
        for user in results:
            users.append( cls(user) )
        return users
