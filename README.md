# Friends Management API
*A simple friends management API built with Flask and MySQL*

## Up and Running
#### 1. Run app with Python
  ```
    source venv/bin/activate
    python app.py
  ```
#### 2. Or run with `gunicorn` server
  ```
    source start.sh
  ```
  or
  ```
    source venv/bin/activate
    gunicorn --bind 0.0.0.0:8000 wsgi:app
  ```
#### 3. Test  
  Run test in virtual environment
  ```
    source venv/bin/activate
    python test.py
  ```

---
## Overview of the designs
### 1. Technical decisions
  * [Python Flask](http://flask.pocoo.org/) is used for quick installation and fast deployment with high flexibility and scalability
  * [SQLAlchemy](https://www.sqlalchemy.org/) is used and wired up with flask using `flask-sqlalchemy` for easier ORM
  * On the server, the app is running on a WSGI `gunicorn` server for better performance, especially with the use of multiple workers for handling concurrent requests
  * Request handling process:
    * App getting request with view functions that are mapped to url patterns in `routes.py`
    * View functions are imported from `middleware.py`, where the main request handling processes take place.
    * View functions in `middleware.py` use data service methods in `store.py` for data-related operations.


### 2. Project Structure
  * Main application files:
    * `app.py` contains the main `app` instance
    * `routes.py` contains all url mapping with route functions
    * `middleware.py` contains all route functions for handling requests and response
    * `store.py` contains data-related methods for read/write/update database directly
    * `model/*` is the folder contains data model created with `SQLAlchemy`
  * Other files:
    * `test.py` contains all test cases built with Flask test client
    * `wsgi.py` is used for running the server with `gunicorn`

### 3. Database design
  ![alt text](/er_diagram.png "ER Diagram")

---
## Friends API Specifications
### 1. `POST /api/friends/connect` - create friend connection
  * Request data: 
    ```json
      {
        "friends": [
          "andy@example.com",
          "john@example.com"
        ]
      }
    ```
  * Response:
    - Success: `{ "success": true }`
    - Error:
      ```json
        {
          "error": "Error message"
        }
      ```

### 2. `POST /api/friends` - get friend list of email
  * Request data:
    ```json
      {
        "email": "andy@example.com"
      }
    ```
  * Response:
    - Success:
      ```json
        {
          "success": true,
          "friends" : [
            "john@example.com"
          ],
          "count" : 1 
        }
      ```
    - Error:
      ```json
        {
          "error": "Error message"
        }
      ```

### 3. `POST /api/friends/common` - get common friends of users
  * Request data:
    ```json
      {
        "friends": [
          "andy@example.com",
          "john@example.com"
        ]
      }
    ```
  * Response:
    - Success:
      ```json
        {
          "success": true,
          "friends" : [
            "common@example.com"
          ],
          "count" : 1
        }
      ```
    - Error:
      ```json
        {
          "error": "Error message"
        }
      ```

### 4. `POST /api/friends/subscribe` - subscribe to update from an email
  * Request data:
    ```json
      {
        "requestor": "lisa@example.com",
        "target": "john@example.com"
      }
    ```
  * Response:
    - Success:
      ```json
        {
          "success": true
        }
      ```
    - Error:
      ```json
        {
          "error": "Error message"
        }
      ```

### 5. `POST /api/friends/block` - block updates from an email
  * Request data:
    ```json
      {
        "requestor": "andy@example.com",
        "target": "john@example.com"
      }
    ```
  * Response:
    - Success:
      ```json
        {
          "success": true
        }
      ```
    - Error:
      ```json
        {
          "error": "Error message"
        }
      ```

### 6. `POST /api/friends/subscribers` - get all users that can receive updates from a sender
  * Request data:
    ```json
      {
        "sender":  "john@example.com",
        "text": "Hello World! kate@example.com"
      }
    ```
  * Response:
    - Success:
      ```json
        {
          "success": true
          "recipients": [
            "lisa@example.com",
            "kate@example.com"
          ]
        }
      ```
    - Error:
      ```json
        {
          "error": "Error message"
        }
      ```

### HTTP Status Code Used
  * `200` - success
  * `404` - resource not found (eg. user email not valid, user id not valid, etc.)
  * `500` - Internal server error (eg. error while updating database, error while creating new record, etc.)