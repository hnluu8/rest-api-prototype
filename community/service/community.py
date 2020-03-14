from typing import List, Union
from enum import Enum, unique
from community.dao.community import CommunityDao
from community.dao.models import *


@unique
class PostType(Enum):
    QUESTION = 1
    RESPONSE = 2


class CommunityService:
    """

    """
    def __init__(self, dao: CommunityDao, logger):
        self.dao = dao
        self.logger = logger
        self.logger.info(f"CommunityService initialized!")

    def get_users(self) -> List[User]:
        return self.dao.get_users()

    def get_user(self, user_id: int) -> User:
        return self.dao.get_user(user_id)

    def get_questions(self) -> List[Question]:
        return self.dao.get_questions()

    def get_question(self, question_id: int) -> Question:
        return self.dao.get_question(question_id)

    def get_responses(self, question_id: int) -> List[Response]:
        return self.dao.get_responses(question_id)

    def get_bookmarks(self, user_id: int, post_type: PostType) -> Union[List[QuestionBookmark], List[ResponseBookmark]]:
        if post_type == PostType.QUESTION:
            return self.dao.get_question_bookmarks(user_id)
        else:
            return self.dao.get_response_bookmarks(user_id)

    def ask_question(self, asker_id: int, title: str, **kwargs) -> Question:
        asker = self.dao.get_user(asker_id)
        if asker is None:
            raise ValueError(f"Asker '{asker_id}' doesn't exist.")
        return self.dao.create_question(asker, title)

    def respond_question(self, responder_id: int, question_id: int, text: str, **kwargs) -> Response:
        responder = self.dao.get_user(responder_id)
        if responder is None:
            raise ValueError(f"Responder '{responder_id}' doesn't exist.")
        question = self.dao.get_question(question_id)
        if question is None:
            raise ValueError(f"Question '{question_id}' doesn't exist.")
        return self.dao.create_response(responder, question, text)

    def create_bookmark(self, user_id: int, post_id: int, post_type: PostType, **kwargs) -> Union[QuestionBookmark, ResponseBookmark]:
        user = self.dao.get_user(user_id)
        if user is None:
            raise ValueError(f"User '{user_id}' doesn't exist.")
        if post_type == PostType.QUESTION:
            post = self.dao.get_question(post_id)
        else:
            post = self.dao.get_response(post_id)
        if post is None:
            raise ValueError(f"{post_type.name} '{post_id}' doesn't exist.")
        if post_type == PostType.QUESTION:
            return self.dao.create_question_bookmark(user, post)
        else:
            return self.dao.create_response_bookmark(user, post)


