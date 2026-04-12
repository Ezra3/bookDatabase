import unittest
from unittest.mock import patch, mock_open
from FinalProject import Media, Movie, Book, from_dict, get_review, save_entries

class TestMediaApp(unittest.TestCase):

    def test_media_to_dict(self):
        item = Media("Dune", "Sci-Fi", 9)
        self.assertEqual(item.to_dict(), {
            "type": "media",
            "title": "Dune",
            "genre": "Sci-Fi",
            "review": 9
        })

    def test_movie_to_dict(self):
        item = Movie("Inception", "Sci-Fi", 10, "Nolan")
        self.assertEqual(item.to_dict(), {
            "type": "movie",
            "title": "Inception",
            "genre": "Sci-Fi",
            "review": 10,
            "director": "Nolan"
        })

    def test_book_to_dict(self):
        item = Book("Holes", "Fiction", 8, "Sachar")
        self.assertEqual(item.to_dict(), {
            "type": "book",
            "title": "Holes",
            "genre": "Fiction",
            "review": 8,
            "author": "Sachar"
        })

    def test_from_dict_movie(self):
        data = {
            "type": "movie",
            "title": "Inception",
            "genre": "Sci-Fi",
            "review": 10,
            "director": "Nolan"
        }
        item = from_dict(data)
        self.assertIsInstance(item, Movie)

    def test_from_dict_book(self):
        data = {
            "type": "book",
            "title": "Holes",
            "genre": "Fiction",
            "review": 8,
            "author": "Sachar"
        }
        item = from_dict(data)
        self.assertIsInstance(item, Book)

    @patch("builtins.input", side_effect=["abc", "12", "7"])
    def test_get_review(self, mock_input):
        self.assertEqual(get_review(), 7)

    @patch("builtins.open", new_callable=mock_open)
    def test_save_entries(self, mock_file):
        entries = [Movie("Inception", "Sci-Fi", 10, "Nolan")]
        save_entries(entries, filename="test.json")
        mock_file.assert_called_once_with("test.json", "w")

if __name__ == "__main__":
    unittest.main()