import os
import logging
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

from resources.image_detection import ImageDetection

load_dotenv()
app = Flask(__name__, static_folder='static')
CORS(app)
api = Api(app)
app.config['JWT_SECRET_KEY'] = os.environ.get("SECRET_KEY") or "your_default_secret_key"
jwt = JWTManager(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#Mock
users = {
    "admin": {"password": os.environ.get("ADMIN_PASSWORD")}
}


@app.route('/')
def client():
    return render_template('client.html')


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    logger.info("Login attempt received with username: %s", username)
    if not username or not password:
        logger.warning("Login attempt with missing username or password")
        return jsonify({"msg": "Bad username or password"}), 401

    user = users.get(username)
    if user is None or user["password"] != password:
        logger.warning("Login attempt for user: %s failed", username)
        return jsonify({"msg": "Bad username or password"}), 401

    token = create_access_token(identity=username)
    return jsonify({"token": token})


class AuthenticatedImageDetection(ImageDetection):
    decorators = [jwt_required()]

api.add_resource(AuthenticatedImageDetection, '/api/resources/detect')

