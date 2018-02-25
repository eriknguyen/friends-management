from flask import jsonify, request
from store import Store

db_engine = 'mysql+pymysql://root:root@localhost:8889/friends_management'
data_store = Store(db_engine)


def initialize_database():
    data_store.init_database()


# def fill_database():
#     data_store.fill_database()


def user(serialize = True):
    users = data_store.get_users(serialize=serialize)
    if serialize:
        return jsonify({"users": users, "total": len(users)})
    else:
        return users


def user_by_id(id):
    current_user = data_store.get_user_by_id(id, serialize=True)
    if current_user:
        return jsonify({"user": current_user})
    else:
        return jsonify({"error": "User ID is invalid"}), 404


def add_user():
    req_json = request.get_json()
    email = req_json["email"]
    check_user = data_store.get_user_by_email(email, serialize=True)
    if check_user:
        return jsonify({
            'message': 'User is already created.',
            'id': check_user.id
        })
    new_user_id = data_store.add_user(email=email)

    return jsonify({
        "id": new_user_id
    })


def delete_user(id):
    if data_store.delete_user(id):
        return jsonify({
            'message': 'User deleted successfully'
        })
    else:
        return jsonify({
            'error': 'User ID is invalid'
        }), 404


def connect_friends():
    req_json = request.get_json()
    friends = req_json["friends"]
    if data_store.get_user_by_email(friends[0]) is None:
        return jsonify({
            'error': 'User %s is not valid' % friends[0]
        }), 404

    if data_store.get_user_by_email(friends[1]) is None:
        return jsonify({
            'error': 'User %s is not valid' % friends[1]
        }), 404

    try:
        data_store.connect_users(friends[0], friends[1])
        return jsonify({
            'success': True
        })
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error: ' + str(e)
        }), 500


def friends_list():
    req_json = request.get_json()
    email = req_json['email']
    friends = data_store.get_user_friends(email, serialize=True)
    return jsonify({
        'success': True,
        'friends': [u['email'] for u in friends],
        'count': len(friends)
    })


def common_friends():
    req_json = request.get_json()
    friends = req_json["friends"]
    if data_store.get_user_by_email(friends[0]) is None:
        return jsonify({
            'error': 'User %s is not valid' % friends[0]
        }), 404

    if data_store.get_user_by_email(friends[1]) is None:
        return jsonify({
            'error': 'User %s is not valid' % friends[1]
        }), 404

    try:
        common_friends = data_store.get_user_common_friends(friends[0], friends[1])
        return jsonify({
            'success': True,
            'friends': [u.email for u in common_friends],
            'count': len(common_friends)
        })
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error: ' + str(e)
        }), 500


def subscribe():
    pass


def block_friends():
    pass


def subscribers_list():
    pass


def build_message(key, message):
    return {key:message}
