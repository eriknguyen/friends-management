from flask import jsonify, abort, make_response, request
from store import Store

db_engine = 'mysql+pymysql://root:root@localhost:8889/friends_management'
data_store = Store(db_engine)


def initialize_database():
    data_store.init_database()


# def fill_database():
#     data_store.fill_database()


def user(serialize = True):
    users = data_store.get_user(serialize=serialize)
    if serialize:
        return jsonify({"users": users, "total": len(users)})
    else:
        return users


def user_by_id(id):
    current_user = data_store.get_user(id, serialize=True)
    if current_user:
        return jsonify({"user": current_user})
    else:
        abort(404)


def add_user():
    email = request.form["email"]
    new_user_id = data_store.add_user(email=email)

    return jsonify({
        "id": new_user_id
    })


def delete_user(id):
    if data_store.delete_user(id):
        return make_response('', 200)
    else:
        return abort(404)


def build_message(key, message):
    return {key:message}
