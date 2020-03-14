from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, class_mapper
from community.dao import BaseModel


class Question(BaseModel):
    """
        Represents a community question.
    """
    asker_id = Column(Integer, ForeignKey('user.id'), index=True, nullable=False)
    title = Column(String(1000), nullable=False)

    # A user can ask many questions.
    asker = relationship('User', backref='questions', lazy='joined')

    def for_json(self):
        d = self.encode(ignore_columns=['asker_id'])
        d['asker'] = self.asker.encode()
        d['responses'] = [r.encode(ignore_columns=['question_id']) for r in self.responses]
        return d

    def __repr__(self):
        return f"<Question {self.id}>"