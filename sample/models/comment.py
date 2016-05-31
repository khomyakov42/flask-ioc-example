from datetime import datetime


class Comment:
    def __init__(self, id, post_id, author_name: str, text: str, created_at: datetime):
        self.id = id
        self.post_id = post_id
        self.author_name = author_name
        self.text = text
        self.created_at = created_at
