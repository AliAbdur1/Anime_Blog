from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import animes_model # <-- may not need this import
from flask import flash, session
from flask_bcrypt import Bcrypt
from flask_app import app
import re

bcrypt = Bcrypt(app)
#might need other imports like flash other classes and regex

db = 'users_and_animes'

class Users:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.User_anime_list = []
        #follow database table fields plus any other attribute you want to create
        pass


    ## FIND METHODS ##


    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(db).query_db(query)
        all_users = []
        for user in results:
            all_users.append(cls(user))
        print(results)
        return all_users
    
    @classmethod
    def get_user_by_id(cls):
        # data = {'id': user_id} # may need to remove data
        query = "SELECT * FROM users WHERE id = %(id)s;"
        found_user_id = connectToMySQL(db).query_db(query) # may need to remove data
        return found_user_id
    
    @classmethod
    def get_user_by_email(cls, email):
        data = {'email': email}
        query = "SELECT * FROM users WHERE email = %(email)s;"
        user_email = connectToMySQL(db).query_db(query, data)
        if user_email:
            return cls(user_email[0])
        return False
    
        ## CREATE METHODS ##
    
    @classmethod 
    def new_register(cls, data):
        
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);"
        new_user_id = connectToMySQL(db).query_db(query,data)
        session['new_user_id'] = new_user_id 
        session['user_name'] = f'{data["first_name"]} {data["last_name"]}' 
        session['email'] = f'{data["email"]}'
        return new_user_id
    
    #---------------------#
    ## LOGIN AND REG ##
    @staticmethod
    def login(data):
        this_user = Users.get_user_by_email(data['email'])
        if this_user:
            if bcrypt.check_password_hash(this_user.password, data['password']):
                session['new_user_id'] = this_user.id
                session['user_name'] = f'{this_user.first_name} {this_user.last_name}'
                return True
        flash('Your login or password was incorrect')
        return False
    
    @staticmethod
    def registration_validation(user):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # ---------found on stack over flow---------#
        PW_REGEX = re.compile(r'^.*(?=.{8,10})(?=.*[a-zA-Z])(?=.*?[A-Z])(?=.*\d)[a-zA-Z0-9!@£$%^&*()_+={}?:~\[\]]+$')
        # ---------found on stack over flow---------#
        is_valid = True
        if len(user['first_name']) < 2:
            flash("first name is not longer enough. must be at least two characters long.")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("last name is not long enough. must be at least two characters long.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("please use a valid email address")
            is_valid = False
        if not PW_REGEX.match(user['password']):
            flash("Please enter a more secure password. At least 8 characters long, containing 1 Uppercase letter, 1 number and 1 special character")
            is_valid = False
        # if len(user['password']) < 8: # try commenting out the above regex if statment and this one.
        #     flash("password must be a least eight characters long") # try commenting out the above regex if statment and this one.
        #     is_valid = False # try commenting out the above regex if statment and this one.
        if user['password'] != user['confirm_password']:
            flash("password must match confirmation password")
            is_valid = False
        # will return either 
        if Users.get_user_by_email(user['email']):
            flash("Email is already in use by another user")
            is_valid = False # dont forget this return
        return is_valid #... or this one