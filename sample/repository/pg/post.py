import typing
from .base import PgRepository
from sample.repository import PostRepository
from sample.models import Post


class PgPostRepository(PgRepository, PostRepository):
    def delete(self, post) -> bool:
        with self.connection.cursor() as c:
            c.execute('''
                delete from posts where id = %s
            ''', (post.id,))
            return c.rowcount > 0

    def create(self, post: Post):
        with self.connection.cursor() as c:
            c.execute('''
                insert into posts(title, author_name, text, created_at)
                values(%s, %s, %s, %s)
                returning id
            ''', (post.id, post.author_name, post.text, post.created_at))
            post.id = c.fetchone()['id']
            return post

    def find_by_page(self, page, per_page) -> typing.List[Post]:
        offset = (page - 1) * per_page
        with self.connection.cursor() as c:
            c.execute('''
                select * from posts offset %s limit %s
            ''', (offset, per_page))
            return list(map(self.parse_row, c.fetchall()))

    def get(self, id) -> Post:
        with self.connection.cursor() as c:
            c.execute('''
                select * from posts where id = %s
            ''', (id, ))
            if c.rowcount > 0:
                return self.parse_row(c.fetchone())
            return None

    def parse_row(self, row) -> Post:
        return Post(**row)

