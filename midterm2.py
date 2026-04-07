from abc import ABC, abstractmethod

class Device(ABC):
    def __init__(self, brand):
        self.brand = brand

    @abstractmethod
    def show_info(self):
        pass


class Phone(Device):
    def __init__(self, brand, screen_size, camera_mp, supports_5g):
        super().__init__(brand)
        self.screen_size = screen_size
        self.camera_mp = camera_mp
        self.supports_5g = supports_5g

    def show_info(self):
        print("Phone Info")
        print(f"Brand: {self.brand}")
        print(f"Screen Size: {self.screen_size} inches")
        print(f"Camera: {self.camera_mp} MP")
        print(f"5G Support: {'Yes' if self.supports_5g else 'No'}")


class Tablet(Device):
    def __init__(self, brand, screen_size, has_stylus, storage_gb):
        super().__init__(brand)
        self.screen_size = screen_size
        self.has_stylus = has_stylus
        self.storage_gb = storage_gb

    def show_info(self):
        print("Tablet Info")
        print(f"Brand: {self.brand}")
        print(f"Screen Size: {self.screen_size} inches")
        print(f"Stylus Support: {'Yes' if self.has_stylus else 'No'}")
        print(f"Storage: {self.storage_gb} GB")


class Laptop(Device):
    def __init__(self, brand, ram_gb, storage_gb, processor):
        super().__init__(brand)
        self.ram_gb = ram_gb
        self.storage_gb = storage_gb
        self.processor = processor

    def show_info(self):
        print("Laptop Info")
        print(f"Brand: {self.brand}")
        print(f"RAM: {self.ram_gb} GB")
        print(f"Storage: {self.storage_gb} GB")
        print(f"Processor: {self.processor}")


phone_brand = input("Enter phone brand: ")
tablet_brand = input("Enter tablet brand: ")
laptop_brand = input("Enter laptop brand: ")

phone = Phone(phone_brand, 6.5, 48, True)
tablet = Tablet(tablet_brand, 10.9, True, 128)
laptop = Laptop(laptop_brand, 16, 512, "Intel i7")


phone.show_info()
print()
tablet.show_info()
print()
laptop.show_info()


class Book:
    all_books = []

    def __init__(self, title, author, ISBN):
        self.title = title
        self.author = author
        self.ISBN = ISBN
        Book.all_books.append(self)

    def display_info(self):
        print(f"Title: {self.title}")
        print(f"Author: {self.author}")
        print(f"ISBN: {self.ISBN}")

    @classmethod
    def search_by_author(cls, author_name):
        return [book for book in cls.all_books if book.author.lower() == author_name.lower()]


book1 = Book("The Great Gatsby", "F. Scott Fitzgerald", "978-0743273565")
book2 = Book("To Kill a Mockingbird", "Harper Lee", "978-0061120084")
book3 = Book("1984", "George Orwell", "978-0451524935")
book4 = Book("Animal Farm", "George Orwell", "978-0451526342")

print("\nBook Details:")
for book in Book.all_books:
    book.display_info()
    print()

author_to_search = "George Orwell"
matched_books = Book.search_by_author(author_to_search)

print(f"Books by {author_to_search}:")
if matched_books:
    for book in matched_books:
        book.display_info()
        print()
else:
    print("No books found.")


class shape(ABC):
    @abstractmethod
    def area(self):
        pass
class triangle(shape):
    def __init__(self, base, height):
        self.base = base
        self.height = height

    def area(self):
        return 0.5 * self.base * self.height
class rectangle(shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height
class circle(shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius ** 2


class ImageAlbum:
    def __init__(self):
        self.images = []

    def add_image(self, width, height):
        self.images.append({
            "size": (width, height),
            "coordinates": None
        })

    def arrange_images(self, max_row_width=20, gap=1):
        x = 0
        y = 0
        row_height = 0

        for image in self.images:
            width, height = image["size"]

            if x + width > max_row_width:
                x = 0
                y += row_height + gap
                row_height = 0

            image["coordinates"] = (x, y)
            x += width + gap
            row_height = max(row_height, height)

    def print_image_coordinates(self):
        for index, image in enumerate(self.images, start=1):
            width, height = image["size"]
            x, y = image["coordinates"] if image["coordinates"] is not None else (None, None)
            print(f"Image {index}: size=({width}, {height}), coordinates=({x}, {y})")


album = ImageAlbum()
album.add_image(5, 4)
album.add_image(7, 3)
album.add_image(6, 5)
album.add_image(4, 2)
album.add_image(8, 4)

album.arrange_images(max_row_width=20, gap=1)
print("\nArranged Image Coordinates:")
album.print_image_coordinates()


class Duck:
    def quack(self):
        print("Quack! Quack!")


class Person:
    def quack(self):
        print("I can't quack, but I can mimic!")


def check_quack_behavior(obj):
    if hasattr(obj, "quack") and callable(getattr(obj, "quack")):
        obj.quack()
    else:
        print("This object doesn't quack!")


duck = Duck()
person = Person()
number = 42
text = "hello"

print("\nDuck Typing Check:")
check_quack_behavior(duck)
check_quack_behavior(person)
check_quack_behavior(number)
check_quack_behavior(text)
