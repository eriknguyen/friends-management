from app import app
import unittest, json


class AppTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_index(self):
        resp = self.app.get('/')
        json_data = self.get_json(resp)
        assert resp.status == "200 OK"
        assert json_data['status'] == 'OK'

    # test cases for friends-management
    def test_connect(self, email_1=None, email_2=None):
        email_1 = email_1 or 'andy@example.com'
        email_2 = email_2 or 'john@example.com'
        self.test_create_users(email_1)
        self.test_create_users(email_2)
        req_json = {
            'friends': [
                email_1,
                email_2
            ]
        }
        resp = self.app.post('/api/friends/connect', data=json.dumps(req_json), content_type='application/json')
        data = self.get_json(resp)
        assert data['success'] is not None
        assert data['success'] is True

    def test_get_friendlist(self):
        req_json = {
            'email': 'andy@example.com'
        }
        resp = self.app.post('/api/friends', data=json.dumps(req_json), content_type='application/json')
        data = self.get_json(resp)
        assert data['success'] == True
        # assert len(data['friends']) > 0
        # assert 'john@example.com' in data['friends']
        assert data['count'] == len(data['friends'])

    def test_get_common_friends(self, email_1=None, email_2=None):
        email_1 = email_1 or 'andy@example.com'
        email_2 = email_2 or 'john@example.com'
        common_email = 'common@example.com'
        self.test_create_users(common_email)
        self.test_connect(email_1=email_1, email_2=common_email)
        self.test_connect(email_1=email_2, email_2=common_email)
        req_json = {
            'friends': [
                email_1,
                email_2
            ]
        }
        resp = self.app.post('/api/friends/common', data=json.dumps(req_json), content_type='application/json')
        data = self.get_json(resp)
        assert data['success'] is True
        assert common_email in data['friends']
        assert data['count'] == len(data['friends'])
        assert data['count'] > 0

    def test_subscribe_friend(self, requestor=None, target=None):
        requestor = requestor or "lisa@example.com"
        target = target or "john@example.com"
        self.test_create_users(requestor)
        self.test_create_users(target)
        req_json = {
            "requestor": requestor,
            "target": target
        }
        resp = self.app.post('api/friends/subscribe', data=json.dumps(req_json), content_type='application/json')
        data = self.get_json(resp)
        assert data['success'] == True

    def test_block_friend(self, requestor=None, target=None):
        requestor = requestor or "andy@example.com"
        target = target or "john@example.com"
        req_json = {
            "requestor": requestor,
            "target": target
        }
        resp = self.app.post('api/friends/block', data=json.dumps(req_json), content_type='application/json')
        data = self.get_json(resp)
        assert data['success'] == True

    def test_get_subscribers(self):
        sender = "john@example.com"
        mentioned_subscriber = 'kate@example.com'
        friend_subscriber = 'common@example.com'
        blocked_friend = "andy@example.com"
        self.test_create_users(mentioned_subscriber)
        req_json = {
            "sender":  sender,
            "text": "Hello World! " + mentioned_subscriber
        }
        resp = self.app.post('api/friends/subscribers', data=json.dumps(req_json), content_type='application/json')
        data = self.get_json(resp)
        assert data['success'] == True
        assert friend_subscriber in data['recipients']
        assert mentioned_subscriber in data['recipients']
        assert blocked_friend not in data['recipients']

    # end test cases for friends-management

    # basic test cases for users
    def test_get_users(self):
        resp = self.app.get('/api/users')
        json_data = self.get_json(resp)
        assert type(json_data["total"]) == int

    def test_create_users(self, email=None):
        email = email or 'test_user@example.com'
        resp = self.app.post('/api/users', data=json.dumps(dict(email=email)),
                             content_type='application/json')
        data = self.get_json(resp)
        assert data['id'] is not None

    def test_get_user_by_id(self, id=None, email=None):
        id = id or 3
        email = email or 'test_user@example.com'
        resp = self.app.get('/api/users/' + str(id))
        data = self.get_json(resp)
        assert data['user'] is not None
        user = data['user']
        assert user['id'] is not None
        assert user['email'] is not None

    # end basic test cases for users

    def get_json(self, resp):
        return json.loads(resp.data.decode())


if __name__ == '__main__':
    unittest.main()
