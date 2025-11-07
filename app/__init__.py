from flask import Flask
from storage.storage import Storage

app = Flask(__name__)
storage = Storage("logs.db", "data/schema.sql")

from app import routes
