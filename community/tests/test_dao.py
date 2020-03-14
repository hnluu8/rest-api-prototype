from community.dao.community import CommunityDao


class TestDao(object):
    def test_create_question(self, dao: CommunityDao):
        asker = dao.get_user(1)
        question = dao.create_question(asker, "How do you keep the weight off?")
        assert(question.asker.id == asker.id)

    def test_create_response(self, dao: CommunityDao):
        responder = dao.get_user(2)
        question = dao.get_question(1)
        assert(len(question.responses) == 0)

        response = dao.create_response(responder, question, "Diet and exercise.")
        assert(response.question_id == question.id and response.responder_id == responder.id)

    def test_get_question_and_response(self, dao: CommunityDao):
        question = dao.get_question(1)
        assert(len(question.responses) == 1)

    def test_create_bookmarks(self, dao: CommunityDao):
        user = dao.get_user(1)
        assert(len(user.question_bookmarks) == 0)
        assert(len(user.response_bookmarks) == 0)

        # Bookmark question
        question = dao.get_question(1)
        dao.create_question_bookmark(user, question)

        # Bookmark response
        response = dao.get_response(1)
        dao.create_response_bookmark(user, response)

        user = dao.get_user(1)
        assert(len(user.question_bookmarks) == 1)
        assert(len(user.response_bookmarks) == 1)

