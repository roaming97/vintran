import logging
import os

from dotenv import load_dotenv
from flask import Flask
from flask_apscheduler import APScheduler
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

db = SQLAlchemy()
app = Flask(__name__, template_folder="./html")

load_dotenv(override=True)

app.config["SECRET_KEY"] = os.getenv("SECRET")
app.config["MAX_CONTENT_LENGTH"] = 100_000_000  # 100MiB
# PRODUCTION: Only enable this if the connection is strictly HTTPS, otherwise the site will not work correctly
# app.config['SESSION_COOKIE_SECURE'] = True
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

blocked_ips = os.getenv("BLOCKED_IPV4")
blocked_ips = blocked_ips.split(",") if blocked_ips else []

csrf = CSRFProtect(app=app)
CORS(app=app)
db.init_app(app=app)
scheduler = APScheduler()

with app.app_context():
    if not os.path.exists(os.getenv("DATABASE_URI")):
        db.create_all()

logging.basicConfig(
    filename="vintran.log",
    filemode="w",
    format="%(levelname)s - %(message)s",
    level=logging.DEBUG,
)
logging.getLogger(app.logger.name)
logging.debug(blocked_ips)

from vintran import forms, models, routes
