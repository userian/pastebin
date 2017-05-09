import pastebin
import unittest
import uuid

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.app = pastebin.app.test_client()

    def tearDown(self):
        print("all done!")
        
    def test_index_get(self):
        response = self.app.get('/')
        assert response.status_code == 200

    def test_index_post(self):
        response = self.app.post('/', data=dict(data='this is data'))
        assert response.status_code == 302
        assert 'Location' in response.headers

    def test_bin_get(self):
        data = 'this quick brown fox'
        response = self.app.post('/', data=dict(data=data))

        bin_link = response.headers['Location']
        response = self.app.get(bin_link)

        # There's a bunch of other HTML so just make sure it's in there
        assert data in response.data

    def test_bin_get_440(self):
        response = self.app.get('/bin/' + str(uuid.uuid4()))
        assert response.status_code == 404

    # TODO
    # test encryption 
    # posting not non-existent bin should 404 (I don't think it does right now)
    # posting to a bucket should over write existing

if __name__ == '__main__':
    unittest.main()