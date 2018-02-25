from flask import jsonify

from middleware import user_by_id, user, add_user, delete_user
from middleware import initialize_database as init_db
from middleware import build_message


def init_api_routes(app):
    if app:
        app.add_url_rule('/', 'index', index, methods=['GET'])
        app.add_url_rule('/api/users/<string:id>', 'user_by_id', user_by_id, methods=['GET'])
        app.add_url_rule('/api/users', 'user', user, methods=['GET'])
        app.add_url_rule('/api/users', 'add_user', add_user, methods=['POST'])
        app.add_url_rule('/api/users/delete/<string:id>', 'delete_user', delete_user, methods=['DELETE'])

        app.add_url_rule('/api/initdb', 'initdb', initialize_database)
        app.add_url_rule('/api', 'list_routes', list_routes, methods=['GET'], defaults={'app': app})


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
