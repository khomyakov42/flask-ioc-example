import typing
import abc
from .base import Repository
from sample.models import Post


class PostRepository(Repository):
    @abc.abstractmethod
    def create(self, post: Post) -> Post:
        raise NotImplementedError()

    @abc.abstractmethod
    def get(self, id) -> Post:
        raise NotImplementedError()

    @abc.abstractmethod
    def find_by_page(self, page, per_page) -> typing.List[Post]:
        raise NotImplementedError()

    @abc.abstractmethod
    def delete(self, post) -> bool:
        raise NotImplementedError()