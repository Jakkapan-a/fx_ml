import os

from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from dotenv import load_dotenv
import logging
from logging.handlers import TimedRotatingFileHandler
from flask_cors import CORS
db = SQLAlchemy()
migrate = Migrate()
def create_app():
    app = Flask(__name__)
    load_dotenv()
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.config.from_object(Config)

    if not os.path.exists('migrations'):
        os.makedirs('migrations')

    # Logging
    if not os.path.exists('logs'):
        os.makedirs('logs')
    handler = TimedRotatingFileHandler(app.config['LOG_FILE'], when="midnight", interval=1)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.info("Starting server...")



    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    # Import models
    from app.models import forex_data

    # migrate init db
    # @app.before_request()
    # def create_tables():
    #     print("Creating tables...")
        # db.create_all()

    # Register blueprints
    @app.route('/')
    def index():
        return jsonify({'message': 'Welcome to the API!'})

    from app.routes import v1_0_0_bp
    app.register_blueprint(v1_0_0_bp, url_prefix='/api/v1.0.0')

    return app