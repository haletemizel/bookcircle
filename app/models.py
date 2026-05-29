from datetime import datetime
from typing import Optional, List
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app

from app import db, login

club_members = db.Table('club_members',
    db.Column('user_id', db.Integer, ForeignKey('user.id'), primary_key=True),
    db.Column('club_id', db.Integer, ForeignKey('book_club.id'), primary_key=True)
)

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, ForeignKey('user.id'), primary_key=True),
    db.Column('followed_id', db.Integer, ForeignKey('user.id'), primary_key=True)
)

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(64), index=True, unique=True)
    email: Mapped[str] = mapped_column(String(120), index=True, unique=True)
    avatar_file: Mapped[str] = mapped_column(String(20), default='default.jpg', server_default='default.jpg')
    about_me: Mapped[Optional[str]] = mapped_column(db.Text)
    password_hash: Mapped[Optional[str]] = mapped_column(String(256))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    reading_progresses: Mapped[List["ReadingProgress"]] = relationship(back_populates="user")
    clubs: Mapped[List["BookClub"]] = relationship(secondary=club_members, back_populates="members")
    reviews: Mapped[List["Review"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    followed: Mapped[List["User"]] = relationship(
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        back_populates="followers"
    )
    followers: Mapped[List["User"]] = relationship(
        secondary=followers,
        primaryjoin=(followers.c.followed_id == id),
        secondaryjoin=(followers.c.follower_id == id),
        back_populates="followed"
    )

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return user in self.followed

    def get_reset_password_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_password_token(token, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, max_age=expires_sec)['user_id']
        except Exception:
            return None
        return db.session.get(User, user_id)

    def __repr__(self):
        return f"<User {self.username}>"

class Book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(140))
    author: Mapped[str] = mapped_column(String(140))
    total_pages: Mapped[int]
    genre: Mapped[Optional[str]] = mapped_column(String(64))
    series_name: Mapped[Optional[str]] = mapped_column(String(140))
    volume_number: Mapped[Optional[int]]
    image_url: Mapped[Optional[str]] = mapped_column(String(255))
    summary: Mapped[Optional[str]] = mapped_column(db.Text)

    reading_progresses: Mapped[List["ReadingProgress"]] = relationship(back_populates="book")
    reviews: Mapped[List["Review"]] = relationship(back_populates="book", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Book '{self.title}' by {self.author}>"

class ReadingProgress(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    book_id: Mapped[int] = mapped_column(ForeignKey('book.id'))
    current_page: Mapped[int] = mapped_column(default=0)
    status: Mapped[str] = mapped_column(String(20), default="Okunuyor")

    user: Mapped["User"] = relationship(back_populates="reading_progresses")
    book: Mapped["Book"] = relationship(back_populates="reading_progresses")

    def __repr__(self):
        return f"<ReadingProgress User:{self.user_id} - Book:{self.book_id} [{self.status}]>"

class BookClub(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(140), index=True, unique=True)
    description: Mapped[Optional[str]] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    creator_id: Mapped[int] = mapped_column(ForeignKey('user.id'))

    members: Mapped[List["User"]] = relationship(secondary=club_members, back_populates="clubs")
    messages: Mapped[List["ClubMessage"]] = relationship(back_populates="club", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<BookClub {self.name}>"

class ClubMessage(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    body: Mapped[str] = mapped_column(String(1000))
    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    club_id: Mapped[int] = mapped_column(ForeignKey('book_club.id'))

    user: Mapped["User"] = relationship()
    club: Mapped["BookClub"] = relationship(back_populates="messages")

    def __repr__(self):
        return f"<ClubMessage {self.body[:20]}>"

class Review(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    body: Mapped[str] = mapped_column(db.Text)
    rating: Mapped[int] = mapped_column(db.Integer)
    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    book_id: Mapped[int] = mapped_column(ForeignKey('book.id'))

    user: Mapped["User"] = relationship(back_populates="reviews")
    book: Mapped["Book"] = relationship(back_populates="reviews")

    def __repr__(self):
        return f"<Review {self.rating} stars for Book {self.book_id}>"
