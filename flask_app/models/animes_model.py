from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import users_model
from flask_app import app
from flask import flash, session
from flask_bcrypt import Bcrypt
import re

bcrypt = Bcrypt(app)

db = 'users_and_animes'

class Animes:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.plot = data['plot']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id'] #<-- still not sure i need foreign key here
        self.reviews = [] ## added on 8/13/23 from discord suggest
        self.posted_by = None


    ## get anime by id update? VV
    @classmethod
    def get_anime_by_id(cls, id):
        data = {'id': id}
        query = """
            SELECT animes.*, users.*, reviews.review_of_anime 
            FROM animes
            LEFT JOIN users ON animes.user_id = users.id
            LEFT JOIN reviews ON animes.id = reviews.anime_id
            WHERE animes.id = %(id)s;
        """
        results = connectToMySQL(db).query_db(query, data)
        
        if not results:
            return None
        
        anime_data = results[0]
        new_anime = cls(anime_data)
        user_data = {
            'id': anime_data['users.id'],
            'first_name': anime_data['first_name'],
            'last_name': anime_data['last_name'],
            'email': anime_data['email'],
            'password': anime_data['password'],
            'created_at': anime_data['users.created_at'],
            'updated_at': anime_data['users.updated_at'],
        }
        new_anime.posted_by = users_model.Users(user_data)
        
        # Add reviews to the anime object
        new_anime.reviews = []
        for result in results: # should this be anime_data instead of result?
            if result['review_of_anime']:
                review = {
                    'user_id': result['user_id'],
                    'user_first_name': result['first_name'],
                    'review_of_anime': result['review_of_anime'],
                }
                new_anime.reviews.append(review)
        
        return new_anime
    ## get anime by id update? ^^
    
    @classmethod
    def get_all_animes(cls):
        query = 'SELECT * FROM animes LEFT JOIN users ON animes.user_id = users.id;'
        results = connectToMySQL(db).query_db(query)
        user_animes = []
        for this_anime in results:
            new_anime = cls(this_anime)
            this_anime_poster = {
                'id': this_anime['users.id'],
                'first_name': this_anime['first_name'],
                'last_name': this_anime['last_name'],
                'email': this_anime['email'],
                'password': this_anime['password'],
                'created_at': this_anime['created_at'], 
                'updated_at': this_anime['updated_at'],
            }
            new_anime.posted_by = users_model.Users(this_anime_poster)
            user_animes.append(new_anime)
        return user_animes
    
    @classmethod
    def get_anime_w_user(cls, id):
        data = {'id' : id}
        query = 'SELECT * FROM animes LEFT JOIN users ON animes.user_id = users.id WHERE animes.id = %(id)s;'
        results = connectToMySQL(db).query_db(query, data)
        
        new_anime = cls(results[0])
        this_user = {
            'id': results[0]['users.id'],
            'first_name': results[0]['first_name'],
            'last_name': results[0]['last_name'],
            'email': results[0]['email'],
            'password': results[0]['password'],
            'created_at': results[0]['created_at'],
            'updated_at': results[0]['updated_at'],
        }
        new_anime.posted_by = users_model.Users(this_user)
        return new_anime
    
    
    ## ADD METHODS ##
    @classmethod
    def add_an_anime(cls, new_anime_data):

        query = "INSERT INTO animes (title, plot, user_id) VALUES (%(title)s,%(plot)s,%(user_id)s);"
        result = connectToMySQL(db).query_db(query, new_anime_data)
        return result
    
    ## possible bugs? VV

    @classmethod
    def add_anime_review(cls, anime_id, user_id, review_text):
        query = """
        INSERT INTO reviews (anime_id, user_id, review_of_anime)
        VALUES (%(anime_id)s, %(user_id)s, %(review_of_anime)s);
        """
        review_data = {
        'anime_id': anime_id,
        'user_id': user_id,
        'review_of_anime': review_text,
        }
        result = connectToMySQL(db).query_db(query, review_data)
        return result

    
    ## EDIT METHODS ##
    @classmethod
    def edit_anime_by_id(cls, anime_data):
        query = "UPDATE animes SET title=%(title)s, plot=%(plot)s WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, anime_data)
        return results
    

    ## VALIDATION FOR EDIT ##
    @staticmethod
    def validate_anime_entry(feature):
        is_valid = True
        if len(feature['title']) < 2:
            flash("anime must be longer than two characters")
            is_valid = False
        if len(feature['plot']) < 2:
            flash("plot specification must be at least two characters log")
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_anime_towatch(anime):
        is_valid = True
        if len(anime['title']) < 2:
            flash("title must be longer than three characters")
            is_valid = False
        if len(anime['plot']) < 2:
            flash("plot specification must be at least two characters log")
            is_valid = False
        return is_valid
    



    ## DELETE METHODS ##
    @classmethod
    def delete_anime(cls, del_data):
        query = "DELETE FROM animes WHERE id = %(id)s;"
        data = {'id': del_data}
        connectToMySQL(db).query_db(query, data)
        return