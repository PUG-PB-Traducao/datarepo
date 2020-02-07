from datetime import datetime
from uuid import uuid4

from bcrypt import checkpw, gensalt, hashpw
from sqlalchemy import (Boolean, Column, DateTime, Enum, ForeignKey, Integer,
                        String)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, autoincrement=True, primary_key=True)
    password = Column(String(128), nullable=False)
    last_login = Column(DateTime, nullable=False)
    username = Column(String(150), nullable=False, unique=True)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(150), nullable=False)
    email = Column(String(254), nullable=False)
    is_active = Column(Boolean, nullable=False)
    last_login = Column(
        DateTime, nullable=False,
        default=datetime.utcnow().strptime("%d-%m-%y %H:%M:%S"))
    registered_at = Column(
        DateTime, nullable=False,
        default=datetime.utcnow().strptime("%d-%m-%y %H:%M:%S"))
    permission_id = Column(
        Integer, ForeignKey('permissions.id'),
        nullable=False)
    post_id = Column(
        Integer, ForeignKey('posts.id'),
        nullable=False)

    permission = db.relationship('Permissions')
    post = db.relationship('Post')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.password = self.generate_password_hash(self.password)

    def __repr__(self):
        return f"<User: {self.username}>"

    def compare_password(self, password):
        return checkpw(password.encode('utf8'), self.password.encode('utf8'))

    def generate_password_hash(self, password):
        return hashpw(password.encode('utf8'), gensalt()).decode('utf8')


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, autoincrement=True, primary_key=True)
    role_id = Column(
        Integer, ForeignKey('roles.id'),
        nullable=False)
    user_id = Column(
        Integer, ForeignKey('users.id'),
        nullable=False)

    user = db.relationship('User')
    post = db.relationship('Role')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, autoincrement=True, primary_key=True)
    description = Column(String)
    created_at = Column(
        DateTime, nullable=False,
        default=datetime.utcnow().strptime("%d-%m-%y %H:%M:%S"))
    is_admin = Column(Boolean, nullable=False)
    permission_id = Column(
        Integer, ForeignKey('permissions.id'),
        nullable=False)
    permission = db.relationship('Permission')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, autoincrement=True, primary_key=True)
    uuid = Column(UUID(as_uuid=True), default=uuid4, unique=True)
    user_id = Column(
        Integer, ForeignKey('users.id'),
        nullable=False)
    link = Column(String)
    translate_notification = Column(Boolean, nullable=False)
    translate_link = Column(String)
    translated_link = Column(String)
    likes = Column(Integer, default=0)
    created_at = Column(
        DateTime, nullable=False,
        default=datetime.utcnow().strptime("%d-%m-%y %H:%M:%S"))
    approved_at = Column(DateTime, nullable=False)
    approved_by = Column(
        Integer, ForeignKey('users.id'),
        nullable=True)
    user = db.relationship('User')
    approver = db.relationship('User')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
