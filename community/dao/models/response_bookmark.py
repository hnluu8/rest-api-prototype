from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from community.dao import BaseModel


class ResponseBookmark(BaseModel):
    """
        Represents a bookmarked response.
    """
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    response_id = Column(Integer, ForeignKey('response.id'), nullable=False)

    __table_args__ = (UniqueConstraint('user_id', 'response_id', name='user_response_idx'),)

    # A user can bookmark many questions.
    user = relationship('User', backref='response_bookmarks', lazy='joined')

    # A question can be bookmarked many times.
    response = relationship('Response', backref='bookmarks', lazy='joined')

    def for_json(self):
        d = self.encode(ignore_columns=['user_id', 'response_id'])
        d['user'] = self.user.encode()
        d['response'] = self.response.encode()
        return d

    def __repr__(self):
        return f"<ResponseBookmark {self.id}>"