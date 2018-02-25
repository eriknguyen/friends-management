from flask import jsonify

from middleware import user_by_id, user, add_user, delete_user
from middleware import connect_friends, friends_list, common_friends, subscribe, block_friends, subscribers_list
from middleware import initialize_database as init_db
from middleware import build_message


def init_api_routes(app):
    if app:
        app.add_url_rule('/', 'index', index, methods=['GET'])
        app.add_url_rule('/api/initdb', 'initdb', initialize_database)
        app.add_url_rule('/api', 'list_routes', list_routes, methods=['GET'], defaults={'app': app})
        init_api_users(app)
        init_api_friends(app)


def init_api_users(app):
    app.add_url_rule('/api/users/<string:id>', 'user_by_id', user_by_id, methods=['GET'])
    app.add_url_rule('/api/users', 'user', user, methods=['GET'])
    app.add_url_rule('/api/users', 'add_user', add_user, methods=['POST'])
    app.add_url_rule('/api/users/delete/<string:id>', 'delete_user', delete_user, methods=['DELETE'])


def init_api_friends(app):
    app.add_url_rule('/api/friends/connect', 'connect_friens', connect_friends, methods=['POST'])
    app.add_url_rule('/api/friends', 'friendlist', friends_list, methods=['POST'])
    app.add_url_rule('/api/friends/common', 'common_friends', common_friends, methods=['POST'])
    app.add_url_rule('/api/friends/subscribe', 'subscribe_friends', subscribe, methods=['POST'])
    app.add_url_rule('/api/friends/block', 'block_friends', block_friends, methods=['POST'])
    app.add_url_rule('/api/friends/subscribers', 'subscribers_list', subscribers_list, methods=['POST'])


def index():
    return jsonify({
        'status': 'OK'
    })


def list_routes(app):
    result = []
    for rt in app.url_map.iter_rules():
        result.append({
            'methods': list(rt.methods),
            'route': str(rt)
        })
    return jsonify({'routes': result, 'total': len(result)})


def initialize_database():
    message_key = "Initialize Database"
    try:
        init_db()
    except ValueError as err:
        return jsonify(build_message(message_key, err.message))

    return jsonify(build_message(message_key, "OK"))


'''
def fill_database():
    message_key = "Fill Database"
    try:
        fill_db()
    except ValueError as err:
        return jsonify(build_message(message_key, err.message))

    return jsonify(build_message(message_key, "OK"))
'''
