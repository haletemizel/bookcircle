from datetime import datetime
from typing import Optional, List
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import db

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(64), index=True, unique=True)
    email: Mapped[str] = mapped_column(String(120), index=True, unique=True)
    password_hash: Mapped[Optional[str]] = mapped_column(String(256))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    reading_progresses: Mapped[List["ReadingProgress"]] = relationship(back_populates="user")

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"

class Book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(140))
    author: Mapped[str] = mapped_column(String(140))
    total_pages: Mapped[int]
    genre: Mapped[Optional[str]] = mapped_column(String(64))

    reading_progresses: Mapped[List["ReadingProgress"]] = relationship(back_populates="book")

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
