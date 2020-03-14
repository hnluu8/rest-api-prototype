from typing import List
from sqlalchemy.orm import Session, joinedload
from community.dao.models import *


class CommunityDao:
    """
        Data layer with reusable SQLAlchemy models.
    """
    def __init__(self, db_session: Session, logger):
        self.db_session = db_session
        self.logger = logger
        self.logger.info(f"CommunityDao initialized!")

    def get_users(self) -> List[User]:
        return self.db_session.query(User).all()

    def get_user(self, user_id: int) -> User:
        return self.db_session.query(User)\
            .options(joinedload(User.question_bookmarks), joinedload(User.response_bookmarks))\
            .filter(User.id == user_id).one()

    def get_question(self, question_id: int) -> Question:
        return self.db_session.query(Question)\
            .options(joinedload(Question.responses))\
            .filter(Question.id == question_id).one()

    def get_questions(self) -> List[Question]:
        return self.db_session.query(Question).all()

    def get_response(self, response_id: int) -> Response:
        return self.db_session.query(Response).get(response_id)

    def get_responses(self, question_id: int) -> List[Response]:
        return self.db_session.query(Response).filter_by(question_id=question_id).all()

    def get_question_bookmarks(self, user_id: int) -> List[QuestionBookmark]:
        return self.db_session.query(QuestionBookmark).filter_by(user_id=user_id).all()

    def get_response_bookmarks(self, user_id: int) -> List[ResponseBookmark]:
        return self.db_session.query(ResponseBookmark).filter_by(user_id=user_id).all()

    def create_question(self, asker: User, title: str, **kwargs) -> Question:
        question = Question(title=title)
        question.asker = asker
        self.db_session.add(question)
        self.db_session.commit()
        self.db_session.refresh(question)
        return question

    def create_response(self, responder: User, question: Question, text: str, **kwargs) -> Response:
        response = Response(text=text)
        response.responder = responder
        response.question = question
        self.db_session.add(response)
        self.db_session.commit()
        self.db_session.refresh(response)
        return response

    def create_question_bookmark(self, user: User, question: Question) -> QuestionBookmark:
        bookmark = QuestionBookmark()
        bookmark.user = user
        bookmark.question = question
        self.db_session.add(bookmark)
        self.db_session.commit()
        self.db_session.refresh(bookmark)
        return bookmark

    def create_response_bookmark(self, user: User, response: Response) -> ResponseBookmark:
        bookmark = ResponseBookmark()
        bookmark.user = user
        bookmark.response = response
        self.db_session.add(bookmark)
        self.db_session.commit()
        self.db_session.refresh(bookmark)
        return bookmark
