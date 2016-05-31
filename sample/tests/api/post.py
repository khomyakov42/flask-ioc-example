import typing
from datetime import datetime
from flask.ext.api import FlaskAPI
from flask.ext.testing import TestCase
import inject
from sample.repository import PostRepository, CommentRepository
from sample.repository.base import Transaction, Repository
from sample.models import Post, Comment


class FakeRepository(Repository):
    def set_transaction(self, tx: typing.Union[Transaction, None]):
        pass


class FakePostRepository(PostRepository, FakeRepository):
    rows = []

    def get(self, id) -> Post:
        for row in self.rows:
            if row['id'] == id:
                return Post(**row)
        return None

    def create(self, post: Post) -> Post:
        self.rows.append(post.__dict__)

    def delete(self, post: Post) -> bool:
        for row in self.rows:
            if row['id'] == post.id:
                self.rows.remove(row)
                return True
        return False

    def find_by_page(self, page, per_page) -> typing.List[Post]:
        return list(map(lambda row: Post(**row), self.rows[(page - 1) * per_page:][:per_page]))


class FakeCommentRepository(CommentRepository, FakeRepository):
    rows = []

    def delete(self, comment: Comment) -> bool:
        for row in self.rows:
            if row['id'] == comment.id:
                self.rows.remove(row)
                return True
        return False

    def create(self, comment: Comment):
        self.rows.append(comment.__dict__)

    def find_by_post_id(self, post_id) -> typing.List[Comment]:
        return list(map(lambda row: Comment(**row), filter(lambda row: row['post_id'] == post_id, self.rows)))


class PostApiTestCase(TestCase):
    post_rows = [dict(
       id=i,
       title='',
       author_name='',
       text='',
       created_at=datetime.now()
    ) for i in range(100)]

    def create_app(self):
        self.post_repository = FakePostRepository()
        self.post_repository.rows = self.post_rows

        self.comment_repository = FakeCommentRepository()

        inject.clear_and_configure(lambda binder: binder
                                   .bind(PostRepository, self.post_repository)
                                   .bind(CommentRepository, self.comment_repository))

        from sample.api.posts import app as post_api

        self.app = FlaskAPI(__name__)
        self.app.config['TESTING'] = True
        self.app.register_blueprint(post_api, url_prefix='')
        self.client = self.app.test_client()
        return self.app

    def assertPostResource(self, data):
        for field in ('id', 'author_name', 'title', 'text', 'created_at'):
            self.assertIn(field, data)

    def test_get_post_list_without_page(self):
        resp = self.client.get('/posts')
        self.assert200(resp)
        self.assertIsInstance(resp.json, list)
        self.assertEqual(len(resp.json), 20)
        for post in resp.json:
            self.assertPostResource(post)

    def test_get_post_list_with_negative_page(self):
        resp = self.client.get('/posts?page=-1')
        self.assert400(resp)

    def test_get_post_list_with_invalid_page(self):
        resp = self.client.get('/posts?page=lolka')
        self.assert400(resp)
