from app import app
import unittest, json

class AppTestCase(unittest.TestCase):
  def setUp(self):
    print("[TEST] Setting up the env for tests!")
    app.config['TESTING'] = True
    self.app = app.test_client()

  def tearDown(self):
    print("[TEST] Tearing down after tests!")

  def test_index(self):
    resp = self.app.get('/')
    json_data = self.get_json(resp)
    assert resp.status == "200 OK"
    assert json_data['status'] == 'OK'

  def test_get_users(self):
    resp = self.app.get('/api/users')
    json_data = self.get_json(resp)
    assert type(json_data["total"]) == int

  def test_create_users(self):
    resp = self.app.post('/api/users', data = json.dumps(dict(email="test_user@example.com")), content_type='application/json')
    data = self.get_json(resp)
    assert data['id'] is not None

  def test_get_user_by_id(self, id=None, email=None):
    id = id or 5
    email = email or 'test_user@example.com'
    resp = self.app.get('/api/users/' + str(id))
    data = self.get_json(resp)
    assert data['user'] is not None
    user = data['user'][0]
    if email:
      assert user['email'] == email
    else:
      assert user['email'] is not None

  def get_json(self, resp):
    return json.loads(resp.data.decode())

if __name__ == '__main__':
  unittest.main()