import os


class Book:

    def __init__(self, title: str, author: str):
        self._title = title
        self._author = author
        self._is_borrowed = False

    def view_info(self):
        print(
            f"Title: {self._title} - {'Not avaible' if self._is_borrowed else 'Avaible'}"
        )
        print(f"Author: {self._author}")

    @property
    def title(self):
        return self._title

    @property
    def is_borrowed(self):
        return self._is_borrowed

    @is_borrowed.setter
    def is_borrowed(self, is_borrowed: bool):
        self._is_borrowed = is_borrowed


class Library:

    def __init__(self):
        self.books = []

    def add_book(self, title: str, author: str):
        book = Book(title, author)
        self.books.append(book)

    def take_book(self, title: str):
        for book in self.books:
            if title == book.title:

                if book.is_borrowed:
                    print(f"The book {title} is not avaible")
                    return

                book.is_borrowed = True
                print(f"Book '{title}' has been borrowed. Enjoy Reading")
                return
        else:
            print(f"The book {title} is not on list")

    def view_books(self):
        if not self.books:
            print("No books in the library.")
        else:
            print("\n--- Library Catalog ---")
            for book in self.books:
                book.view_info()

    def return_book(self, title: str):
        for book in self.books:
            if title == book.title and book.is_borrowed:
                book.is_borrowed = False
                print(f"Book '{title}' has been returned.")
                return
        else:
            print(f"Book '{title}' is not in the library.")


def main():

    library = Library()

    while True:
        os.system("cls")
        print("Library Management System")
        print("1. Add Book")
        print("2. View Books")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            title = input("Enter book title: ").strip()
            author = input("Enter author name: ").strip()
            library.add_book(title, author)
            input("Press Enter to continue...")

        elif choice == "2":
            library.view_books()
            input("Press Enter to continue...")

        elif choice == "3":
            title = input("Enter book title to borrow: ").strip()
            library.take_book(title)
            input("Press Enter to continue...")

        elif choice == "4":
            title = input("Enter book title to return: ").strip()
            library.return_book(title)
            input("Press Enter to continue...")

        elif choice == "5":
            print("Exiting the program.")
            break


if __name__ == "__main__":
    main()
