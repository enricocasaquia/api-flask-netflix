from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from flask import make_response, render_template
from models.user import UserModel
from blacklist import BLACKLIST
    
class User(Resource):
    @jwt_required()
    def get(self, id):
        """
        Find an user by the correspondent id
        ---
        tags:
          - Users
        parameters:
          - in: path
            name: id
            type: integer
            required: true
            description: user id
        responses:
          200:
            description: User found
          404:
            description: User not found
        """
        user = UserModel.find_user_id(id)
        if user:
            return {
                'user': user.json(),
                'message': 'User found.'
            }, 200
        return {'message':'User not found.'}, 404
    
    @jwt_required()
    def delete(self, id):
        """
        Deletes an user
        ---
        tags:
          - Users
        parameters:
          - in: path
            name: id
            type: integer
            required: true
            description: user id
        responses:
          200:
            description: User successfully deleted
          404:
            description: User not found
          500:
            description: Error deleting user
        """
        user = UserModel.find_user_id(id)
        if user:
            try:
                user.delete_user()
                return {
                    'user': user.json(),
                    'message': 'User successfully deleted.'
                }, 200
            except Exception as e:
                print(f"Error deleting user: {e}")
                return {'message': 'Error deleting user.'}, 500
        else: return {'message':'User not found.'}, 404
        
class UserSignon(Resource):
    def post(self):
        """
        Inserts a new user
        ---
        tags:
          - Users
        parameters:
          - in: body
            name: body
            schema:
              type: object
              properties:
                login:
                  type: string
                password:
                  type: string
                email:
                  type: string
        responses:
          201:
            description: User successfully inserted
          409:
            description: Login {login} already exists
          500:
            description: Error inserting user
        """
        data = UserModel.parse_user()
        if not data['email'] or data['email'] is None:
            return {'message':'The field email is required.'}, 400
        if UserModel.find_user_login(data['login']):
            return {'message':'Login {} already exists.'.format(data['login'])}, 409
        if UserModel.find_user_email(data['email']):
            return {'message':'Email {} already exists.'.format(data['email'])}, 409
        user = UserModel(**data)
        user.active = False
        try:
            user.insert_user()
            user.send_confirmation_email()
            return {
                'user': user.json(),
                'message': 'User successfully inserted.'
            }, 201
        except Exception as e:
            user.delete_user()
            print(f"Error inserting user: {e}")
            return {'message': 'Error inserting user.'}, 500
    
    @jwt_required()
    def patch(self):
        """
        Updates an user
        ---
        tags:
          - Users
        parameters:
          - in: body
            name: body
            schema:
              type: object
              properties:
                login:
                  type: string
                password:
                  type: string
                email:
                  type: string
                active:
                  type: string
        responses:
          200:
            description: User successfully updated
          404:
            description: User not found
          500:
            description: Error updating user
        """
        data = UserModel.parse_user()
        user = UserModel.find_user_login(data['login'])
        if user:
            try:
                user.update_user(**data)
                return {
                    'user': user.json(),
                    'message': 'User successfully updated.'
                }, 200
            except Exception as e:
                print(f"Error updating user: {e}")
                return {'message': 'Error updating user.'}, 500
        else: return {'message':'User not found.'}, 404

class UserLogin(Resource):
    @classmethod
    def post(cls):
        """
        User login
        ---
        tags:
          - Users
        parameters:
          - in: body
            name: body
            schema:
              type: object
              properties:
                login:
                  type: string
                password:
                  type: string
        responses:
          200:
            description: {token}
          401:
            description: Login or password are invalid
          409:
            description: Inactive user
        """
        data = UserModel.parse_user()
        user = UserModel.find_user_login(data['login'])
        if user and UserModel.check_password(data['password'],user.password):
            if user.active == True:
                token = create_access_token(identity=user.id)
                return {
                    'token': token
                }, 200
            return {'message': 'Inactive user.'}, 409
        return {'message': 'Login or password are invalid.'}, 401
    
class UserLogout(Resource):
    @jwt_required()
    def post(self):
        """
        User logout
        ---
        tags:
          - Users
        parameters:
          - in: body
            name: body
            schema:
              type: object
        responses:
          200:
            description: User successfully logged out
          500:
            description: Error logging out
        """
        jwt = get_jwt()['jti']
        if jwt:
            BLACKLIST.add(jwt)
            return {'message':'User successfully logged out.'}, 200
        return {'message': 'Error logging out.'}, 500
            
class UserConfirm(Resource):
    @classmethod
    def get(cls,id):
      user = UserModel.find_user_id(id)
      if not user:
        response = make_response(render_template('user_notfound.html'), 404)
        response.headers['Content-Type'] = 'text/html'
        return response
      if user.active == False:
        user.active = True
        user.insert_user() #Na realidade faz o update
        response = make_response(render_template('user_confirmation.html', email=user.email, usuario=user.login), 200)
        response.headers['Content-Type'] = 'text/html'
        return response
      response = make_response(render_template('user_confirmed.html', email=user.email, usuario=user.login), 200)
      response.headers['Content-Type'] = 'text/html'
      return response