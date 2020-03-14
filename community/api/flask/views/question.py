from flask import Blueprint, request
from community.api.container import IocContainer
from community.service.community import CommunityService
from community.api.flask import response


question_api = Blueprint('questions', __name__, url_prefix='/api/v1/questions')
community_service: CommunityService = IocContainer.community_service()


@question_api.route('', methods=['GET'])
def get_questions():
    """

    :return:
    """
    result = community_service.get_questions()
    return response.json_success(result)


@question_api.route('/<question_id>', methods=['GET'])
def get_question(question_id: int):
    """

    :param question_id:
    :return:
    """
    result = community_service.get_question(question_id)
    return response.json_success(result)


@question_api.route('/<question_id>/responses', methods=['GET'])
def get_responses(question_id: int):
    """

    :param question_id:
    :return:
    """
    result = community_service.get_responses(question_id)
    return response.json_success(result)


@question_api.route('', methods=['POST'])
def create_question():
    """

    :return:
    """
    payload = request.get_json(force=True)
    if 'asker_id' not in payload:
        return response.json_failure("Missing asker_id", status=400)
    if 'title' not in payload:
        return response.json_failure("Missing title", status=400)
    result = community_service.ask_question(payload['asker_id'], payload['title'])
    return response.json_success(result, status=201)


@question_api.route('/<question_id>/responses', methods=['POST'])
def create_response(question_id: int):
    """

    :param question_id:
    :return:
    """
    payload = request.get_json(force=True)
    if 'responder_id' not in payload:
        return response.json_failure("Missing responder_id", status=400)
    if 'text' not in payload:
        return response.json_failure("Missing text", status=400)
    result = community_service.respond_question(payload['responder_id'], question_id, payload['text'])
    return response.json_success(result, status=201)

