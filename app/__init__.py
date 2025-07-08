from config import SECRET_KEY
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
from app import routes