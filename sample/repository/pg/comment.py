import typing
from .base import PgRepository
from sample.repository import CommentRepository
from sample.models import Comment


class PgCommentRepository(PgRepository, CommentRepository):
    def delete(self, comment: Comment) -> bool:
        with self.connection.cursor() as c:
            c.execute('''
                delete from comments where id = %s
            ''', (comment.id, ))
            return c.rowcount > 0

    def create(self, comment: Comment):
        with self.connection.cursor() as c:
            c.execute('''
                insert into comments(post_id, author_name, text)
                values (%s, %s, %s)
                returning id
            ''', (comment.post_id, comment.author_name, comment.text))
            comment.id = c.fetchone()['id']
            return comment

    def find_by_post_id(self, post_id) -> typing.List[Comment]:
        with self.connection.cursor() as c:
            c.execute('''
                select comments.* from post_comments
                right join comments on post_comments.post_id = %s and post_comments.comment_id = comments.id
            ''', (post_id, ))

            return list(map(self.parse_row, c.fetchall()))

    def parse_row(self, row):
        return Comment(**row)

