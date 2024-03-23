import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config_by_name

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    config_name = os.environ.get('APP_CONFIG_NAME', 'development')
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import user_routes
    app.register_blueprint(user_routes.bp)

    return app
