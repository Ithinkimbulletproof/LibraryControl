import json
import os


class Book:
    """Класс, представляющий книгу."""

    def __init__(self, book_id: int, title: str, author: str,
                 year: int, status: str = "в наличии"):
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self):
        """Преобразует объект книги в словарь для сериализации в JSON."""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status
        }


class Library:
    """Класс для управления библиотекой."""

    def __init__(self, filename: str):
        self.filename = filename
        self.books = self.load_books()

    def load_books(self):
        """Загружает книги из файла."""
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                return [Book(**book) for book in json.load(f)]
        return []

    def save_books(self):
        """Сохраняет книги в файл."""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump([book.to_dict() for book in self.books], f,
                      ensure_ascii=False, indent=4)

    def add_book(self, title: str, author: str, year: int):
        """Добавляет книгу в библиотеку."""
        book_id = len(self.books) + 1  # Генерация уникального ID
        new_book = Book(book_id, title, author, year)
        self.books.append(new_book)
        self.save_books()

    def delete_book(self, book_id: int):
        """Удаляет книгу из библиотеки по ID."""
        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)
                self.save_books()
                return
        print("Книга с таким ID не найдена.")

    def search_books(self, query: str):
        """Ищет книги по заголовку, автору или году издания."""
        results = [book for book in self.books if
                   query in book.title or query in book.author or query in str(
                       book.year)]
        return results

    def display_books(self):
        """Отображает все книги в библиотеке."""
        for book in self.books:
            print(
                f"ID: {book.id}, Title: {book.title}, Author: {book.author}, Year: {book.year}, Status: {book.status}")

    def update_status(self, book_id: int, new_status: str):
        """Изменяет статус книги по ID."""
        if new_status not in ["в наличии", "выдана"]:
            print(
                "Неверный статус. Статус может быть только 'в наличии' или 'выдана'.")
            return
        for book in self.books:
            if book.id == book_id:
                book.status = new_status
                self.save_books()
                return
        print("Книга с таким ID не найдена.")


def menu():
    library = Library('library.json')

    while True:
        print("\n1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Поиск книги")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("0. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = int(input("Введите год издания: "))
            library.add_book(title, author, year)

        elif choice == "2":
            book_id = int(input("Введите ID книги: "))
            library.delete_book(book_id)

        elif choice == "3":
            query = input(
                "Введите название, автора или год для поиска: ")
            results = library.search_books(query)
            if results:
                for book in results:
                    print(
                        f"ID: {book.id}, Title: {book.title}, Author: {book.author}, Year: {book.year}, Status: {book.status}")
            else:
                print("Книги не найдены.")

        elif choice == "4":
            library.display_books()

        elif choice == "5":
            book_id = int(input("Введите ID книги: "))
            new_status = input(
                "Введите новый статус ('в наличии' или 'выдана'): ")
            library.update_status(book_id, new_status)

        elif choice == "0":
            break

        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    menu()
