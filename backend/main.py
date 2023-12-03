from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

# Создание сервера на фласк
app = Flask(__name__)
# Создание апишки
api = Api(app)


app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Секретный ключ для JWT
jwt = JWTManager(app)

# Пример базы данных (SQLite)
users = {'user1': {'password': 'password1'}, 'user2': {'password': 'password2'}}

# регистрация
class Register(Resource):
#     метод пост с json
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']
# юзера нет
        if username in users:
            return {'message': 'User already exists'}, 400
# юзер есть
        users[username] = {'password': password}
        return {'message': 'User created successfully'}, 201

# логин
class Login(Resource):
# метод пост
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']
# нет юзера или пароль не тот
        if username not in users or users[username]['password'] != password:
            return {'message': 'Invalid credentials'}, 401
# выдаем токен
        access_token = create_access_token(identity=username)
        return {'access_token': access_token}

# Защищенный ресурс (требует токена)
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        return {'message': f'Hello, {current_user}! This is a protected resource.'}

api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(ProtectedResource, '/protected')

if __name__ == '__main__':
    app.run(debug=True)
