class Library:
    def __init__(self):
        self.books = {}  # Hash Map → ISBN: Title
        self.borrow_stack = []  # Stack

    def add_book(self, isbn, title):
        self.books[isbn] = {
            "title": title,
            "available": True
        }

    def borrow_book(self, isbn):
        if isbn not in self.books:
            return "Book not found"

        if not self.books[isbn]["available"]:
            return "Book already borrowed"

        self.books[isbn]["available"] = False
        self.borrow_stack.append(isbn)

        return f"{self.books[isbn]['title']} borrowed"

    def return_book(self):
        if not self.borrow_stack:
            return "No books to return"

        isbn = self.borrow_stack.pop()
        self.books[isbn]["available"] = True

        return f"{self.books[isbn]['title']} returned"

    def get_books(self):
        return self.books