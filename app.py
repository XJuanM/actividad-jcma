from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask (___name___)


USER_DB = ''
PASS_DB = ''
URL_DB = ''
NAME_DB = ''

FULL_URL_DB = f'mysql+pymysql://{USER_DB}:{PASS_DB}'