from flask import Flask, jsonify, request
from utils.constants import Settings
from database.database import get_db
from flask_migrate import Migrate
from routes import register_routes
from database.connection import db
from flask_cors import CORS

app = Flask(__name__)
migrate = Migrate(app, db)
register_routes(app)

allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://www.test-presupuesto.naoweesuite.com"
]

CORS(
    app,
    origins=allowed_origins,
    supports_credentials=True
)
@app.before_request
def before_request():
    with get_db() as db:
        request.db = db


@app.route('/')
def index():
    return jsonify({"data":"Hello World, this api is the inventory api!"} ), 200

if __name__ == '__main__':  
    app.run(host=Settings.HOST, port=Settings.PORT, debug=bool(Settings.DEBUG))