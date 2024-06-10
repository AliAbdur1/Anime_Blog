from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import animes_model

db = 'users_and_animes'

class Reviews:
    def __init__(self, data):
        # self.anime_id = data['anime_id'] <-- may not need
        # self.user_id = data['user_id'] <-- may not need
        self.review_of_anime = data['review_of_anime']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.reviewed_by = [] # <-- this may need to be None

    @classmethod
    def get_review_by_id(cls, id):
        data = {'id': id}
        query = "SELECT * FROM reviews WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0])
    

    ## method may be incorrect ## vv
    # @classmethod
    # def get_reviews_w_anime(cls, review_data):
    #     query = 'SELECT * FROM reviews LEFT JOIN animes ON reviews.anime_id = animes.id LEFT JOIN users ON reviews.user_id = users.id WHERE reviews.id = %(id)s;'
    #     # query = 'SELECT * FROM reviews LEFT JOIN reviews ON reviews.anime_id = animes.id LEFT JOIN animes ON reviews.user_id = users.id WHERE rewiews.id = %(id)s;'
    #     results = connectToMySQL(db).query_db(query, review_data)
    #     review_found = cls(results[0])
    #     this_anime = {
    #         'id': results[0]['animes.id'],
    #         'title': results[0]['title'],
    #         'plot': results[0]['plot'],
    #         'created_at': results[0]['created_at'],
    #         'updated_at': results[0]['updated_at'],
    #     }
    #     review_found.reviewed_by.append(animes_model.Anime(this_anime))

    @classmethod
    def get_reviews_w_anime(cls, review_data):
        query = 'SELECT * FROM reviews LEFT JOIN animes ON reviews.anime_id = animes.id LEFT JOIN users ON reviews.user_id = users.id WHERE reviews.id = %(id)s;'
        # 'SELECT * FROM reviews LEFT JOIN animes ON reviews.anime_id = animes.id 
        # LEFT JOIN users ON reviews.user_id = users.id WHERE reviews.id = %(id)s;'
        results = connectToMySQL(db).query_db(query, review_data)
        reviewed_animes = []
        for r_anime in results:
            review_found = cls(r_anime)
            this_anime = {
                'id': r_anime['animes.id'],
                'title': r_anime['title'],
                'plot': r_anime['plot'],
                'created_at': r_anime['created_at'],
                'updated_at': r_anime['updated_at'],
            }
            review_found.reviewed_by = animes_model.Animes(this_anime)
            reviewed_animes.append(review_found)
        return reviewed_animes

    
    ## ADD METHODS ##
    @classmethod
    def add_review_of_an_anime(cls, anime_review_data):
        # if new_show_data['veiwer_id'] != session['new_veiwer_id']: # may need to comment out
        #     return False # may need to comment out
        query = "INSERT INTO reviews (anime_id, user_id, review_of_anime) VALUES (%(anime_id)s,%(user_id)s,%(review_of_anime)s);"
        result = connectToMySQL(db).query_db(query, anime_review_data)
        return result
    ## ADD METHODS END ##
    
    ## EDIT METHODS ##
    @classmethod
    def edit_review_by_id(cls, review_data):
        query = "UPDATE reviews SET review_of_anime=%(review_of_anime)s WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, review_data)
        return results
    ## EDIT METHODS END ##

        ## DELETE METHODS ##
    @classmethod
    def delete_anime(cls, del_data):
        query = "DELETE FROM animes WHERE id = %(id)s;"
        data = {'id': del_data}
        connectToMySQL(db).query_db(query, data)
        return
