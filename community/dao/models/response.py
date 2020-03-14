from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from community.dao import BaseModel


class Response(BaseModel):
    """
        Represents a response to a question.
    """
    question_id = Column(Integer, ForeignKey('question.id'), index=True, nullable=False)
    responder_id = Column(Integer, ForeignKey('user.id'), index=True, nullable=False)
    text = Column(Text, nullable=False)

    # A question can have many responses.
    question = relationship('Question', backref='responses', lazy='joined')

    # A user can have many responses.
    responder = relationship('User', backref='responses', lazy='joined')

    def __repr__(self):
        return f"<Response {self.id}>"