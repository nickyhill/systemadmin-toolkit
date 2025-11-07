from flask import Flask
from flask_cors import CORS
from storage.storage import Storage

app = Flask(__name__)
CORS(app)
storage = Storage("logs.db", "storage/schema.sql")

from app import routes
