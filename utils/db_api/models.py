from sqlalchemy import (Column, Integer, BigInteger, String, Text, Boolean)
from sqlalchemy import sql
from .database import db


class User(db.Model):
    __tablename__ = 'users'
    query: sql.Select

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = Column(BigInteger, unique=True)
    full_name = Column(String(100))
    username = Column(String(50))

    def __repr__(self):
        return f"<User({self.id=}, {self.full_name=}, {self.username=})>"
