from enum import unique
import json
from flask import Flask, requests, jsonify
from flask_sqlalchemy import SQLAlchemy
import os


flask_app = Flask(__name__)


if __name__ == "__main__":
    flask_app.run(debug=True)


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


@flask_app.route("/items/<id>", methods=["GET"])
def get_item(id):
    item = Item.query.get(id)
    del item.__dict__["_sa_instance_state"]
    return jsonify(item.__dict__)


@flask_app.route("/items", methods=["GET"])
def get_items():
    items = []
    for item in db.session.query(Item).all():
        del item.__dict__["_sa_instance_state"]
        item.append(item.__dict__)
    return jsonify(items)
