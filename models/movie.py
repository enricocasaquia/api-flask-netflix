from flask_restful import reqparse
from sql_alchemy import db
from datetime import datetime
import json

with open("./conf/config.json") as config_json:
    config = json.load(config_json)

class MovieModel(db.Model):
    __tablename__ = config['SQLALCHEMY_MOVIE_TABLE']
    id = db.Column(db.String(7), primary_key = True)
    type = db.Column(db.String(10), nullable = False)
    title = db.Column(db.String(100), nullable = False)
    director = db.Column(db.String(200))
    cast = db.Column(db.String(2000))
    country = db.Column(db.String(100))
    date_added = db.Column(db.DateTime, default=datetime.now())
    release_year = db.Column(db.Integer, nullable = False)
    rating = db.Column(db.String(10))
    duration = db.Column(db.String(15))
    listed_in = db.Column(db.String(200), nullable = False)
    description = db.Column(db.String(9999), nullable = False)
    
    def __init__(self, id, type, title, director, cast, country, release_year, rating, duration, listed_in, description):
        self.id = id
        self.type = type
        self.title = title
        self.director = director
        self.cast = cast
        self.country = country
        self.release_year = release_year
        self.rating = rating
        self.duration = duration
        self.listed_in = listed_in
        self.description = description
    
    @staticmethod
    def parse_movie(id):
        parameters = reqparse.RequestParser()
        parameters.add_argument('id', type=str, required=True, help='The field id cannot be null.')
        parameters.add_argument('type', type=str, required=True, help='The field type cannot be null.')
        parameters.add_argument('title', type=str, required=True, help='The field title cannot be null.')
        parameters.add_argument('director', type=str, help='The field director must be a string.')
        parameters.add_argument('cast', type=str, help='The field cast must be a string.')
        parameters.add_argument('country', type=str, help='The field country must be a string.')
        parameters.add_argument('release_year', type=int, required=True, help='The field release_year cannot be null.')
        parameters.add_argument('rating', type=str, help='The field rating must be a string.')
        parameters.add_argument('duration', type=str, help='The field duration must be a string.')
        parameters.add_argument('listed_in', type=str, required=True, help='The field listed_in cannot be null.')
        parameters.add_argument('description', type=str, required=True, help='The field description cannot be null.')
        data = parameters.parse_args()
        return data
    
    def json(self):
        return {
            'id': self.id,
            'type': self.type,
            'title': self.title,
            'director': self.director,
            'cast': self.cast,
            'country': self.country,
            'date_added': self.convert_datetime_json(self.date_added),
            'release_year': self.release_year,
            'rating': self.rating,
            'duration': self.duration,
            'listed_in': self.listed_in,
            'description': self.description
        }
        
    def convert_datetime_json(self,datetime):
        if datetime is not None:
            return datetime.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        return datetime
        
    @classmethod
    def find_movie(cls,id):
        movie = cls.query.filter_by(id=id).first()
        if movie:
            return movie
        return None
        
    def insert_movie(self):
        db.session.add(self)
        db.session.commit()
        
    def update_movie(self,type,title,release_year,listed_in,description,director=None,cast=None,country=None,rating=None,duration=None):
        self.type = type
        self.title = title
        self.release_year = release_year
        self.listed_in = listed_in
        self.description = description
        if director is not None:
            self.director = director
        if cast is not None:
            self.cast = cast
        if country is not None:
            self.country = country
        if rating is not None:
            self.rating = rating
        if duration is not None:
            self.duration = duration
        db.session.add(self)
        db.session.commit()
        
    def delete_movie(self):
        db.session.delete(self)
        db.session.commit()