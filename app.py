from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import secrets


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


@flask_app.route("/items", methods=["POST"])
def create_item():
    body = request.get_json()
    db.session.add(Item(body["title"], body["content"]))
    db.session.commit()
    return "item created"


@flask_app.route("/items/<id>", methods=["PUT"])
def update_item(id):
    body = request.get_json()
    db.session.query(Item).filter_by(id=id).update(
        dict(title=body["title"], content=body["content"])
    )
    db.session.commit()
    return "item updated"


@flask_app.route("/items/<id>", methods=["DELETE"])
def delete_item(id):
    db.session.query(Item).filter_by(id=id).delete()
    db.session.commit()
    return "item deleted"
