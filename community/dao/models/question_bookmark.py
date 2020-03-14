from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from community.dao import BaseModel


class QuestionBookmark(BaseModel):
    """
        Represents a bookmarked question.
    """
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    question_id = Column(Integer, ForeignKey('question.id'), nullable=False)

    __table_args__ = (UniqueConstraint('user_id', 'question_id', name='user_question_idx'),)

    # A user can bookmark many questions.
    user = relationship('User', backref='question_bookmarks', lazy='joined')

    # A question can be bookmarked many times.
    question = relationship('Question', backref='bookmarks', lazy='joined')

    def for_json(self):
        d = self.encode(ignore_columns=['user_id', 'question_id'])
        d['user'] = self.user.encode()
        d['question'] = self.question.encode()
        return d

    def __repr__(self):
        return f"<QuestionBookmark {self.id}>"