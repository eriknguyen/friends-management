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
    check_user = data_store.get_user_by_email(email)
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
    req_json = request.get_json()
    requestor = req_json["requestor"]
    target = req_json["target"]
    if data_store.get_user_by_email(requestor) is None:
        return jsonify({
            'error': 'Requestor email (%s) is not valid' % requestor
        }), 404

    if data_store.get_user_by_email(requestor) is None:
        return jsonify({
            'error': 'Target email (%s) is not valid' % target
        }), 404

    try:
        data_store.subscribe_user(requestor, target)
        return jsonify({
            'success': True
        })
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error: ' + str(e)
        }), 500


def block_friends():
    req_json = request.get_json()
    requestor = req_json["requestor"]
    target = req_json["target"]
    if data_store.get_user_by_email(requestor) is None:
        return jsonify({
            'error': 'Requestor email (%s) is not valid' % requestor
        }), 404

    if data_store.get_user_by_email(requestor) is None:
        return jsonify({
            'error': 'Target email (%s) is not valid' % target
        }), 404

    try:
        data_store.block_user(requestor, target)
        return jsonify({
            'success': True
        })
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error: ' + str(e)
        }), 500


def subscribers_list():
    req_json = request.get_json()
    sender = req_json["sender"]
    text = req_json["text"]
    if data_store.get_user_by_email(sender) is None:
        return jsonify({
            'error': 'Sender email (%s) is not valid' % sender
        }), 404

    try:
        mentioned_emails = get_mentioned_emails(text)
        mentioned_list = data_store.get_users(email_list=mentioned_emails)
        friends_list = data_store.get_user_friends(sender).all()
        subscribers_list = data_store.get_user_subscribers(sender).all()
        recipients = set([u.email for u in mentioned_list + friends_list + subscribers_list])
        blocked_list = [u.email for u in data_store.get_user_blocked_list(sender).all()]
        for user in blocked_list:
            recipients.remove(user)
        return jsonify({
            'success': True,
            'recipients': list(recipients)
        })
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error: ' + str(e)
        }), 500


def get_mentioned_emails(text):
    result = []
    text = text.strip() + ' '
    at_index = text.find('@')
    if at_index == -1:
        return result
    prev_space_index = at_index - text[:at_index][::-1].find(' ')
    next_space_index = at_index + text[at_index:].find(' ')
    email = text[prev_space_index:next_space_index]
    result.append(email)
    result += get_mentioned_emails(text[next_space_index:])
    return result


def build_message(key, message):
    return {key:message}
