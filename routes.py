from flask import jsonify

def init_api_routes(app):
    if app:
        app.add_url_rule('/', 'index', index, methods=['GET'])


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