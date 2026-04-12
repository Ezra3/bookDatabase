import json

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "media_reviews.json"

def save_entries(entries, filename=DATA_FILE):
    data = [entry.to_dict() for entry in entries]
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

class Media:
    def __init__(self, title, genre, review):
        self.title = title
        self.genre = genre
        self.review = review

    def display(self):
        return f"Title: {self.title}, Genre: {self.genre}, Review: {self.review}/10"

    def to_dict(self):
        return {
            "type": "media",
            "title": self.title,
            "genre": self.genre,
            "review": self.review
        }

def get_media_type():
    while True:
        kind = input("Add a movie or book? ").strip().lower()
        if kind in ("movie", "book"):
            return kind
        print("Invalid input. Please type 'movie' or 'book'.")

class Movie(Media):
    def __init__(self, title, genre, review, director):
        super().__init__(title, genre, review)
        self.director = director

    def display(self):
        return f"Movie | Title: {self.title}, Genre: {self.genre}, Director: {self.director}, Review: {self.review}/10"

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "movie"
        data["director"] = self.director
        return data


class Book(Media):
    def __init__(self, title, genre, review, author):
        super().__init__(title, genre, review)
        self.author = author

    def display(self):
        return f"Book | Title: {self.title}, Genre: {self.genre}, Author: {self.author}, Review: {self.review}/10"

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "book"
        data["author"] = self.author
        return data


def from_dict(data):
    if data["type"] == "movie":
        return Movie(data["title"], data["genre"], data["review"], data["director"])
    elif data["type"] == "book":
        return Book(data["title"], data["genre"], data["review"], data["author"])
    return Media(data["title"], data["genre"], data["review"])


def load_entries(filename="media_reviews.json"):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            return [from_dict(item) for item in data]
    except (FileNotFoundError, json.JSONDecodeError, ValueError, KeyError):
        return []

def get_review():
    while True:
        try:
            review = int(input("Review out of 10: "))
            if 0 <= review <= 10:
                return review
            else:
                print("Please enter a number from 0 to 10.")
        except ValueError:
            print("Please enter a whole number.")

def add_entry(entries):
    kind = get_media_type()
    title = input("Title: ")
    genre = input("Genre: ")
    review = get_review()

    if kind == "movie":
        director = input("Director: ")
        new_item = Movie(title, genre, review, director)
    elif kind == "book":
        author = input("Author: ")
        new_item = Book(title, genre, review, author)
    else:
        print("Invalid type.")
        return

    entries.append(new_item)
    save_entries(entries)
    print("Entry added and saved.")


def search_entries(entries):
    search_title = input("Enter title to search: ").lower()
    found = False

    for entry in entries:
        if entry.title.lower() == search_title:
            print(entry.display())
            found = True

    if not found:
        print("No entry found.")


def edit_entry(entries):
    search_title = input("Enter title to edit: ").lower()

    for entry in entries:
        if entry.title.lower() == search_title:
            print("Current entry:")
            print(entry.display())

            new_title = input("New title (press Enter to keep same): ")
            new_genre = input("New genre (press Enter to keep same): ")
            new_review = input("New review out of 10 (press Enter to keep same): ")

            if new_title:
                entry.title = new_title
            if new_genre:
                entry.genre = new_genre
            if new_review:
                try:
                    review_num = int(new_review)
                    if 0 <= review_num <= 10:
                        entry.review = review_num
                    else:
                        print("Review must be between 0 and 10.")
                except ValueError:
                    print("Review must be a whole number.")

            if isinstance(entry, Movie):
                new_director = input("New director (press Enter to keep same): ")
                if new_director:
                    entry.director = new_director

            elif isinstance(entry, Book):
                new_author = input("New author (press Enter to keep same): ")
                if new_author:
                    entry.author = new_author

            save_entries(entries)
            print("Entry updated and saved.")
            return

    print("No entry found.")


def show_all(entries):
    if not entries:
        print("No entries stored.")
        return

    for entry in entries:
        print(entry.display())


def main():
    entries = load_entries()

    while True:
        print("\n1. Add entry")
        print("2. Search entry")
        print("3. Edit entry")
        print("4. Show all")
        print("5. Quit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_entry(entries)
        elif choice == "2":
            search_entries(entries)
        elif choice == "3":
            edit_entry(entries)
        elif choice == "4":
            show_all(entries)
        elif choice == "5":
            save_entries(entries)
            print("Goodbye.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
