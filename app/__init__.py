from flask import Flask
from storage.storage import Storage

app = Flask(__name__)
storage = Storage("logs.db", "storage/schema.sql")

from app import routes
