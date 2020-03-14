from community.service.community import CommunityService, PostType


class TestService(object):
    def test_create_question(self, service: CommunityService):
        asker = service.get_user(1)
        question = service.ask_question(asker.id, "How do you keep the weight off?")
        assert(question.asker.id == asker.id)

    def test_create_response(self, service: CommunityService):
        responder = service.get_user(2)
        question = service.get_question(1)
        assert(len(question.responses) == 0)

        response = service.respond_question(responder.id, question.id, "Diet and exercise.")
        assert(response.question_id == question.id and response.responder_id == responder.id)

    def test_get_question_and_response(self, service: CommunityService):
        question = service.get_question(1)
        assert(len(question.responses) == 1)

    def test_create_bookmarks(self, service: CommunityService):
        user = service.get_user(1)
        assert(len(user.question_bookmarks) == 0)
        assert(len(user.response_bookmarks) == 0)

        # Bookmark question
        question = service.get_question(1)
        service.create_bookmark(user.id, question.id, PostType.QUESTION)

        # Bookmark response
        response = service.get_responses(question.id)[0]
        service.create_bookmark(user.id, response.id, PostType.RESPONSE)

        user = service.get_user(1)
        assert(len(user.question_bookmarks) == 1)
        assert(len(user.response_bookmarks) == 1)

