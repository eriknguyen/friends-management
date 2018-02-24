from flask import Flask
from routes import init_api_routes

# create the Flask application
app = Flask(__name__)

app.config['SECRET_KEY'] = 'demo-development-server-erik-secret'

init_api_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
