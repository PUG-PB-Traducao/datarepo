from datetime import datetime
from uuid import uuid4

from bcrypt import checkpw, gensalt, hashpw
from sqlalchemy import (Boolean, Column, DateTime, Enum, ForeignKey, Integer,
                        String)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class Permissions(Base):
    __tablename__ = "permissions"

    id = Column(Integer, autoincrement=True, primary_key=True)
    is_staff = Column(Boolean, nullable=False)
    is_superuser = Column(Boolean, nullable=False)
    is_type = Column(
        Enum('admin', 'editor', 'feeder', name='types'),
        nullable=False, server_default=("admin"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, autoincrement=True, primary_key=True)
    password = Column(String(128), nullable=False)
    last_login = Column(DateTime, nullable=False)
    username = Column(String(150), nullable=False, unique=True)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(150), nullable=False)
    email = Column(String(254), nullable=False)
    date_joined = Column(
        DateTime, nullable=False,
        default=datetime.utcnow().strptime("%d-%m-%y %H:%M:%S"))
    permission_id = Column(
        Integer, ForeignKey('permissions.id'),
        nullable=False)

    permission = db.relationship('Permissions')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.password = self.generate_password_hash(self.password)

    def __repr__(self):
        return f"<User: {self.username}>"

    def compare_password(self, password):
        return checkpw(password.encode('utf8'), self.password.encode('utf8'))

    def generate_password_hash(self, password):
        return hashpw(password.encode('utf8'), gensalt()).decode('utf8')


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, autoincrement=True, primary_key=True)
    uuid = Column(UUID(as_uuid=True), default=uuid4, unique=True)
    link = Column(String)
    status = Column(
        Enum('inserted', 'active', 'finished', name='status_types'),
        nullable=False, server_default=("inserted"))
    date_inserted = Column(
        DateTime, nullable=False,
        default=datetime.utcnow().strptime("%d-%m-%y %H:%M:%S"))

    def __init__(self, id, status, link):
        self.id = id
        self.link = link
        self.status = status

    def __repr__(self):
        return f"<Post UUID: {self.uuid}>"


class Selected(Base):
    __tablename__ = "articles"
    id = Column(Integer, autoincrement=True, primary_key=True)
    date_select = Column(DateTime)
    post_id = Column(
        Integer, ForeignKey('users.id'),
        nullable=False)
    user_id = Column(
        Integer, ForeignKey('posts.id'),
        nullable=False)

    user = db.relationship('User')
    post = db.relationship('Post')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

  def __repr__(self):
        return f"<Selected: {self.date_select} to {self.user_id}>"
