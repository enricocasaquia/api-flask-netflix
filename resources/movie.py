from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models.movie import MovieModel
import json

with open("./conf/config.json") as config_json:
    config = json.load(config_json)
    
class Movie(Resource):
    def get(self, id):
        movie = MovieModel.find_movie(id)
        if movie:
            return {
                'movie': movie.json(),
                'message': 'Movie entry found.'
            }, 200
        return {'message':'Movie entry not found.'}, 404
    
    @jwt_required()
    def post(self, id):
        if MovieModel.find_movie(id):
            return {'message':'Id {} already exists.'.format(id)}, 409
        data = MovieModel.parse_movie(id)
        movie = MovieModel(**data)
        try:
            movie.insert_movie()
            return {
                'movie': movie.json(),
                'message': 'Movie entry successfully inserted.'
            }, 201
        except Exception as e:
            print(f"Error inserting movie entry: {e}")
            return {'message': 'Error inserting movie entry.'}, 500
    
    @jwt_required()
    def patch(self, id):
        movie = MovieModel.find_movie(id)
        if movie:
            data = MovieModel.parse_movie(id)
            try:
                movie.update_movie(id,**data)
                return {
                    'hotel': movie.json(),
                    'message': 'Movie entry successfully updated.'
                }, 200
            except Exception as e:
                print(f"Error updating movie entry: {e}")
                return {'message': 'Error updating movie entry.'}, 500
        else: return {'message':'Movie entry not found.'}, 404
    
    @jwt_required()
    def delete(self, id):
        movie = MovieModel.find_movie(id)
        if movie:
            try:
                movie.delete_movie()
                return {
                    'movie': movie.json(),
                    'message': 'Movie entry deleted.'
                }, 200
            except Exception as e:
                print(f"Error deleting movie entry: {e}")
                return {'message': 'Error deleting movie entry.'}, 500
        else: return {'message':'Movie entry not found.'}, 404