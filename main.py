from library import LibrarySystem
from models import BookStatus

if __name__ == "__main__":
    lib = LibrarySystem()

    lib.add_user("U1", "Malak Sameh", "malak@email.com")
    lib.add_book("B1", "Python Programming", "Guido van Rossum", "Technology", 5)

    lib.record_reading("U1", "B1", BookStatus.COMPLETED)

    lib.save_data()