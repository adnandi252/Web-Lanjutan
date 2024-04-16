from flask_jwt_extended import JWTManager, create_access_token

jwt = JWTManager()

def setup_jwt(app):
    app.config['JWT_SECRET_KEY'] = 'secret-key'
    jwt.init_app(app)

def generate_access_token(identity):
    access_token = create_access_token(identity=identity)
    return access_token
