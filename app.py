from enum import unique
from flask import Flask, requests, jsonify
from flask_sqlalchemy import SQLAlchemy
import os


flask_app = Flask(__name__)

flask_app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
db = SQLAlchemy(flask_app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    content = db.Column(db.String(100), unique=True, nullable=False)

    def __init__(self, title, content):
        self.title = title
        self.content = content

    db.create_all()


if __name__ == "__main__":
    flask_app.run(debug=True)
