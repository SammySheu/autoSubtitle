from module.app import app
from flask_jwt_extended import JWTManager

app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config['JWT_SECRET_KEY'] = 'secret'
app.config["JWT_COOKIE_SECURE"] = False

jwt = JWTManager(app)