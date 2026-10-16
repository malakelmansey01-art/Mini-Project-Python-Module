from datetime import datetime
from enum import Enum

class BookStatus(Enum):
    BORROWED = "borrowed"
    COMPLETED = "completed"
    WANT_TO_READ = "want_to_read"

class User:
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.favorite_categories = []

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "favorite_categories": self.favorite_categories
        }

    @classmethod
    def from_dict(cls, data):
        user = cls(data["user_id"], data["name"], data["email"])
        user.favorite_categories = data.get("favorite_categories", [])
        return user


class Book:
    def __init__(self, book_id, title, author, category, available_copies):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.category = category
        self._available_copies = available_copies

    @property
    def available_copies(self):
        return self._available_copies

    @available_copies.setter
    def available_copies(self, value):
        if value < 0:
            raise ValueError("Available copies cannot be negative.")
        self._available_copies = value

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "category": self.category,
            "available_copies": self._available_copies
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["book_id"],
            data["title"],
            data["author"],
            data["category"],
            data["available_copies"]
        )


class Rating:
    def __init__(self, user_id, book_id, score, review=""):
        if not (1 <= score <= 10):
            raise ValueError("Score must be between 1 and 10.")
        self.user_id = user_id
        self.book_id = book_id
        self.score = score
        self.review = review

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "book_id": self.book_id,
            "score": self.score,
            "review": self.review
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["user_id"], data["book_id"], data["score"], data.get("review", ""))


class ReadingHistory:
    def __init__(self, user_id, book_id, date=None, status=BookStatus.WANT_TO_READ):
        self.user_id = user_id
        self.book_id = book_id
        self.date = date if date else datetime.now().strftime("%Y-%m-%d")
        self.status = status if isinstance(status, BookStatus) else BookStatus(status)

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "book_id": self.book_id,
            "date": self.date,
            "status": self.status.value
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["user_id"],
            data["book_id"],
            data["date"],
            BookStatus(data["status"])
        )


class Recommendation:
    def __init__(self, user_id, book_id, reason, score):
        self.user_id = user_id
        self.book_id = book_id
        self.reason = reason
        self.score = score

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "book_id": self.book_id,
            "reason": self.reason,
            "score": self.score
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["user_id"], data["book_id"], data["reason"], data["score"])