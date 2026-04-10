import json
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from FinalProjectRoughDraft import Book, Movie, from_dict, save_entries


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "media_reviews.json"


def entry_from_api(entry):
    if not isinstance(entry, dict):
        raise ValueError("Each entry must be an object.")

    entry_type = entry.get("type")
    title = str(entry.get("title", "")).strip()
    genre = str(entry.get("genre", "")).strip()
    creator = str(entry.get("creator", "")).strip()
    review = entry.get("review")

    if entry_type not in {"book", "movie"}:
        raise ValueError("Entry type must be 'book' or 'movie'.")
    if not title or not genre or not creator:
        raise ValueError("Title, genre, and creator are required.")
    if not isinstance(review, int) or review < 0 or review > 10:
        raise ValueError("Review must be a whole number from 0 to 10.")

    if entry_type == "movie":
        return Movie(title, genre, review, creator)

    return Book(title, genre, review, creator)


def entry_to_api(entry):
    data = entry.to_dict()

    creator = data.get("author")
    if creator is None:
        creator = data.get("director", "")

    return {
        "type": data.get("type"),
        "title": data.get("title", ""),
        "genre": data.get("genre", ""),
        "review": data.get("review"),
        "creator": creator,
    }


def read_entries():
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            raw_entries = json.load(file)
    except (json.JSONDecodeError, OSError):
        return []

    if not isinstance(raw_entries, list):
        return []

    parsed_entries = []
    for raw_entry in raw_entries:
        if not isinstance(raw_entry, dict):
            continue

        try:
            normalized_entry = dict(raw_entry)
            if normalized_entry.get("creator") is not None:
                creator = normalized_entry.get("creator")
                if normalized_entry.get("type") == "book":
                    normalized_entry["author"] = creator
                elif normalized_entry.get("type") == "movie":
                    normalized_entry["director"] = creator
            parsed_entries.append(from_dict(normalized_entry))
        except (ValueError, KeyError, TypeError):
            continue

    return parsed_entries


def write_entries(entries):
    save_entries(entries, DATA_FILE)


class MediaRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def send_json(self, status_code, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/entries":
            self.send_json(200, [entry_to_api(entry) for entry in read_entries()])
            return

        if parsed.path == "/":
            self.path = "/index.html"

        super().do_GET()

    def do_PUT(self):
        parsed = urlparse(self.path)
        if parsed.path != "/api/entries":
            self.send_error(404)
            return

        content_length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_length)

        try:
            payload = json.loads(raw_body.decode("utf-8"))
        except json.JSONDecodeError:
            self.send_json(400, {"error": "Request body must be valid JSON."})
            return

        if not isinstance(payload, list):
            self.send_json(400, {"error": "Request body must be a list of entries."})
            return

        try:
            entries = [entry_from_api(entry) for entry in payload]
        except ValueError as error:
            self.send_json(400, {"error": str(error)})
            return

        write_entries(entries)
        self.send_json(200, [entry_to_api(entry) for entry in entries])


def get_port():
    if len(sys.argv) < 2:
        return 8000

    try:
        port = int(sys.argv[1])
    except ValueError as error:
        raise SystemExit("Port must be a whole number.") from error

    if port < 1 or port > 65535:
        raise SystemExit("Port must be between 1 and 65535.")

    return port


def main():
    port = get_port()
    server = ThreadingHTTPServer(("127.0.0.1", port), MediaRequestHandler)
    print(f"Serving on http://127.0.0.1:{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
