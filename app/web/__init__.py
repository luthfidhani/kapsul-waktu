import redis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from settings import settings


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = settings.sql_alchemy_database_uri
app.config['SECRET_KEY'] = settings.secret_key
db = SQLAlchemy(app)

cache = redis.from_url(settings.redis_uri)

from routes import urls_blueprint
app.register_blueprint(urls_blueprint)
