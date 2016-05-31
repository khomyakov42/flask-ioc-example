from datetime import datetime


class Post:
    def __init__(self, id, author_name: str, title: str, text: str, created_at: datetime):
        self.id = id
        self.author_name = author_name
        self.title = title
        self.text = text
        self.created_at = created_at
