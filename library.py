from collections import Counter
import json
import os
from models import User, Book, Rating, ReadingHistory, Recommendation, BookStatus

class LibrarySystem:
    def __init__(self, storage_file="library_data.json"):
        self.storage_file = storage_file
        self.users = {}
        self.books = {}
        self.ratings = []
        self.history = []
        self.recommendations = []
        self.load_data()

    def add_user(self, user_id, name, email):
        if user_id in self.users:
            print("User ID already exists!")
            return
        self.users[user_id] = User(user_id, name, email)
        print(f"User {name} added successfully.")

    def add_book(self, book_id, title, author, category, available_copies):
        if book_id in self.books:
            print("Book ID already exists!")
            return
        self.books[book_id] = Book(book_id, title, author, category, available_copies)
        print(f"Book '{title}' added successfully.")

    def search_books(self, query):
        query = query.lower()
        results = []
        for book in self.books.values():
            if (query in book.title.lower() or 
                query in book.author.lower() or 
                query in book.category.lower()):
                results.append(book)
        return results

    def add_rating(self, user_id, book_id, score, review=""):
        if user_id not in self.users or book_id not in self.books:
            print("Invalid User ID or Book ID.")
            return
        try:
            rating = Rating(user_id, book_id, score, review)
            self.ratings.append(rating)
            print("Rating added successfully.")
        except ValueError as e:
            print(e)

    def calculate_average_rating(self, book_id):
        book_ratings = [r.score for r in self.ratings if r.book_id == book_id]
        if not book_ratings:
            return 0.0
        return sum(book_ratings) / len(book_ratings)

    def record_reading(self, user_id, book_id, status):
        if user_id not in self.users or book_id not in self.books:
            print("Invalid User ID or Book ID.")
            return
        history_item = ReadingHistory(user_id, book_id, status=status)
        self.history.append(history_item)
        print("Reading record updated.")

    def show_user_history(self, user_id):
        user_records = [h for h in self.history if h.user_id == user_id]
        for h in user_records:
            book = self.books.get(h.book_id)
            book_title = book.title if book else "Unknown"
            print(f"Book: {book_title} | Status: {h.status.value} | Date: {h.date}")

    def detect_read_books(self, user_id):
        completed = [h.book_id for h in self.history if h.user_id == user_id and h.status == BookStatus.COMPLETED]
        return [self.books[b_id] for b_id in completed if b_id in self.books]

    def recommend_books(self, user_id):
        user = self.users.get(user_id)
        if not user:
            print("User not found.")
            return []
        
        read_book_ids = {h.book_id for h in self.history if h.user_id == user_id}
        recommended = []
        
        for book in self.books.values():
            if book.book_id not in read_book_ids:
                avg_score = self.calculate_average_rating(book.book_id)
                if book.category in user.favorite_categories or avg_score >= 7.0:
                    recommended.append(book)
        return recommended

    def get_popular_categories(self):
        categories = [book.category for book in self.books.values()]
        return Counter(categories).most_common()

    def save_data(self):
        data = {
            "users": [u.to_dict() for u in self.users.values()],
            "books": [b.to_dict() for b in self.books.values()],
            "ratings": [r.to_dict() for r in self.ratings],
            "history": [h.to_dict() for h in self.history],
            "recommendations": [rec.to_dict() for rec in self.recommendations]
        }
        with open(self.storage_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("Data saved successfully to JSON.")

    def load_data(self):
        if not os.path.exists(self.storage_file):
            return
        try:
            with open(self.storage_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.users = {u["user_id"]: User.from_dict(u) for u in data.get("users", [])}
                self.books = {b["book_id"]: Book.from_dict(b) for b in data.get("books", [])}
                self.ratings = [Rating.from_dict(r) for r in data.get("ratings", [])]
                self.history = [ReadingHistory.from_dict(h) for h in data.get("history", [])]
                self.recommendations = [Recommendation.from_dict(rec) for rec in data.get("recommendations", [])]
            print("Data loaded successfully from JSON.")
        except Exception as e:
            print(f"Error loading data: {e}")