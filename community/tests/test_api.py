from flask.testing import FlaskClient
import simplejson as json


class TestApi(object):
    def test_create_question(self, client: FlaskClient):
        resp = client.get('/api/v1/users/1')
        assert(resp.status_code == 200)
        user_dict = json.loads(resp.data)['result']

        resp = client.post('/api/v1/questions',
                           data=json.dumps(dict(asker_id=user_dict['id'], title="How do you keep the weight off?")),
                           content_type='application/json')
        assert(resp.status_code == 201)

    def test_create_response(self, client: FlaskClient):
        resp = client.get('/api/v1/users/2')
        assert(resp.status_code == 200)
        responder_dict = json.loads(resp.data)['result']

        resp = client.get('/api/v1/questions/1')
        assert(resp.status_code == 200)
        question_dict = json.loads(resp.data)['result']
        assert(len(question_dict['responses']) == 0)

        resp = client.post(f"/api/v1/questions/{question_dict['id']}/responses",
                           data=json.dumps(dict(responder_id=responder_dict['id'], text="Diet and exercise")),
                           content_type='applicaton/json')
        assert(resp.status_code == 201)
        response_dict = json.loads(resp.data)['result']
        assert(response_dict['question_id'] == question_dict['id'] and response_dict['responder_id'] == responder_dict['id'])

    def test_get_question_and_response(self, client: FlaskClient):
        resp = client.get('/api/v1/questions/1')
        assert(resp.status_code == 200)
        question_dict = json.loads(resp.data)['result']
        assert(len(question_dict['responses']) == 1)

    def test_create_bookmarks(self, client: FlaskClient):
        resp = client.get('/api/v1/users/1')
        assert(resp.status_code == 200)
        user_dict = json.loads(resp.data)['result']
        assert(len(user_dict['bookmarks']) == 0)

        # Bookmark question
        resp = client.get('/api/v1/questions/1')
        assert(resp.status_code == 200)
        question_dict = json.loads(resp.data)['result']
        resp = client.post(f"/api/v1/users/{user_dict['id']}/bookmarks",
                           data=json.dumps(dict(post_type=1, post_id=question_dict['id'])),
                           content_type='application/json')
        assert(resp.status_code == 201)

        # Bookmark response
        resp = client.get(f"/api/v1/questions/{question_dict['id']}/responses")
        assert(resp.status_code == 200)
        response_dict = json.loads(resp.data)['result'][0]
        resp = client.post(f"/api/v1/users/{user_dict['id']}/bookmarks",
                           data=json.dumps(dict(post_type=2, post_id=response_dict['id'])),
                           content_type='application/json')
        assert(resp.status_code == 201)

        resp = client.get(f"/api/v1/users/{user_dict['id']}")
        assert(resp.status_code == 200)
        user_dict = json.loads(resp.data)['result']
        assert(len(user_dict['bookmarks']) == 2)






