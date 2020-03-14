from sqlalchemy import Column, String
from community.dao import BaseModel


class User(BaseModel):
    """
        Represents a community user.
    """
    username = Column(String(15), unique=True, nullable=False)
    name = Column(String(50), nullable=False)

    def for_json(self):
        d = self.encode()
        d['bookmarks'] = [qb.encode(ignore_columns=['user_id']) for qb in self.question_bookmarks] \
                         + [rb.encode(ignore_columns=['user_id']) for rb in self.response_bookmarks]
        return d

    def __repr__(self):
        return f"<User {self.username}>"