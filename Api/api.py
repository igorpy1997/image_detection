import os
import logging

from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

from Resources.ImageDetection import ImageDetection

load_dotenv()
app = Flask(__name__, static_folder='static')
CORS(app)
api = Api(app)
app.config['JWT_SECRET_KEY'] = os.environ.get("SECRET_KEY") or "your_default_secret_key"
jwt = JWTManager(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

users = {
    "admin": {"password": os.environ.get("ADMIN_PASSWORD")}
}


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    logger.info("Login attempt received with username: %s and password: %s", username, password)
    logger.info("Users database: %s", users)  # Логирование состояния users

    if not username or not password:
        logger.warning("Login attempt with missing username or password")
        return jsonify({"msg": "Bad username or password"}), 401

    logger.info("Attempting to authenticate user: %s", username)

    user = users.get(username)
    if user is None or user["password"] != password:
        logger.warning("Login attempt for user: %s failed", username)
        return jsonify({"msg": "Bad username or password"}), 401

    logger.info("User %s logged in successfully", username)
    token = create_access_token(identity=username)
    return jsonify({"token": token})

class AuthenticatedImageDetection(ImageDetection):
    decorators = [jwt_required()]

api.add_resource(AuthenticatedImageDetection, '/api/resources/detect')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
