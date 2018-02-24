# Friends Management API
*A simple friends management API built with Flask and MySQL*

## Up and Running
1. Run app with Python
  ```
    source venv/bin/activate
    python app.py
  ```
2. Or run with `gunicorn` server
  ```
    source start.sh
  ```
  or
  ```
    source venv/bin/activate
    gunicorn --bind 0.0.0.0:8000 wsgi:app
  ```