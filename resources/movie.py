from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models.movie import MovieModel
import json
import sqlite3

with open("./conf/config.json") as config_json_file:
    config_json = json.load(config_json_file)
    
with open("./database/filters.json") as filters_json_file:
    filters_json = json.load(filters_json_file)
    
class Movies(Resource):
    def get(self):
        """
        List all movies or filter by query string
        ---
        tags:
          - Movies
        parameters:
          - in: query
            name: type
            type: string
            required: false
            description: Filter by type (Movie/TV Show)
          - in: query
            name: country
            type: string
            required: false
            description: Filter by country
          - in: query
            name: release_year
            type: integer
            required: false
            description: Filter by release year
          - in: query
            name: rating
            type: string
            required: false
            description: Filter by rating
          - in: query
            name: listed_in
            type: string
            required: false
            description: Filter by genre/category
        responses:
          200:
            description: Movies found
          404:
            description: No movie entries found
          500:
            description: Database error
        """
        filters = {}
        allowed_filters = filters_json['movies']['filters']
        for key in allowed_filters:
            value = request.args.get(key)
            if value:
                filters[key] = value

        movies = []
        try:
            with sqlite3.connect(filters_json['movies']['instance']) as connection:
                cursor = connection.cursor()
                base_query = f"SELECT * FROM {filters_json['movies']['table']}"
                where_clauses = []
                values = []

                for key in filters:
                    if key == 'release_year':
                        where_clauses.append(f"{key} = ?")
                        values.append(filters[key])
                    else:
                        where_clauses.append(f"UPPER({key}) = UPPER(?)")
                        values.append(filters[key])

                if where_clauses:
                    base_query += " WHERE " + " AND ".join(where_clauses)

                result = cursor.execute(base_query, values)
                for line in result:
                    movies.append({
                        'id': line[0],
                        'type': line[1],
                        'title': line[2],
                        'director': line[3],
                        'cast': line[4],
                        'country': line[5],
                        'date_added': line[6],
                        'release_year': line[7],
                        'rating': line[8],
                        'duration': line[9],
                        'listed_in': line[10],
                        'description': line[11]
                    })
        except sqlite3.Error as e:
            return {'message': f'Database error: {str(e)}'}, 500
        if movies:
            return {'movies': movies,
                    'message': 'Movie entries found.'
            }, 200
        return {'message':'No movie entries found.'}, 404
    
class Movie(Resource):
    def get(self, id):
        """
        Find a movie by id
        ---
        tags:
          - Movies
        parameters:
          - in: path
            name: id
            type: string
            required: true
            description: Movie id
        responses:
          200:
            description: Movie entry found
          404:
            description: Movie entry not found
        """
        movie = MovieModel.find_movie(id)
        if movie:
            return {
                'movie': movie.json(),
                'message': 'Movie entry found.'
            }, 200
        return {'message':'Movie entry not found.'}, 404
    
    @jwt_required()
    def post(self, id):
        """
        Insert a new movie
        ---
        tags:
          - Movies
        parameters:
          - in: path
            name: id
            type: string
            required: true
            description: Movie id
          - in: body
            name: body
            schema:
              type: object
              properties:
                id:
                  type: integer
                type:
                  type: string
                title:
                  type: string
                director:
                  type: string
                cast:
                  type: string
                country:
                  type: string
                release_year:
                  type: integer
                rating:
                  type: string
                duration:
                  type: string
                listed_in:
                  type: string
                description:
                  type: string
        responses:
          201:
            description: Movie entry successfully inserted
          409:
            description: Id already exists
          500:
            description: Error inserting movie entry
        """
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
        """
        Update a movie entry
        ---
        tags:
          - Movies
        parameters:
          - in: path
            name: id
            type: string
            required: true
            description: Movie id
          - in: body
            name: body
            schema:
              type: object
              properties:
                type:
                  type: string
                title:
                  type: string
                director:
                  type: string
                cast:
                  type: string
                country:
                  type: string
                release_year:
                  type: integer
                rating:
                  type: string
                duration:
                  type: string
                listed_in:
                  type: string
                description:
                  type: string
        responses:
          200:
            description: Movie entry successfully updated
          404:
            description: Movie entry not found
          500:
            description: Error updating movie entry
        """
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
        """
        Delete a movie entry
        ---
        tags:
          - Movies
        parameters:
          - in: path
            name: id
            type: string
            required: true
            description: Movie id
        responses:
          200:
            description: Movie entry deleted
          404:
            description: Movie entry not found
          500:
            description: Error deleting movie entry
        """
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