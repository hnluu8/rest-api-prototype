from flask import Blueprint, request
from community.api.container import IocContainer
from community.service.community import CommunityService, PostType
from community.api.flask import response


user_api = Blueprint('users', __name__, url_prefix='/api/v1/users')
community_service: CommunityService = IocContainer.community_service()


@user_api.route('', methods=['GET'])
def get_users():
    """

    :return:
    """
    result = community_service.get_users()
    return response.json_success(result)


@user_api.route('/<user_id>', methods=['GET'])
def get_user(user_id: int):
    """

    :param user_id:
    :return:
    """
    result = community_service.get_user(user_id)
    return response.json_success(result)


@user_api.route('<user_id>/bookmarks/<post_type>', methods=['GET'])
def get_bookmarks(user_id: int, post_type: int):
    """

    :param user_id:
    :return:
    """
    try:
        post_type = PostType(post_type)
    except ValueError as e:
        return response.json_failure(f"Invalid post_type '{post_type}'", status=400)

    result = community_service.get_bookmarks(user_id, post_type)
    return response.json_success(result)


@user_api.route('<user_id>/bookmarks', methods=['POST'])
def create_bookmark(user_id: int):
    """

    :param user_id:
    :return:
    """
    payload = request.get_json(force=True)
    if 'post_type' not in payload:
        return response.json_failure("Missing post_type", status=400)
    if 'post_id' not in payload:
        return response.json_failure("Missing post_id", status=400)

    post_id = payload['post_id']
    post_type = payload['post_type']
    try:
        post_type = PostType(post_type)
    except ValueError as e:
        return response.json_failure(f"Invalid post_type '{post_type}'", status=400)

    result = community_service.create_bookmark(user_id, post_id, post_type)
    return response.json_success(result, status=201)


