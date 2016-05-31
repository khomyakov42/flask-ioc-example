import abc
import typing
from .base import Repository
from sample.models import Comment


class CommentRepository(Repository):
    @abc.abstractmethod
    def create(self, comment: Comment):
        raise NotImplementedError()

    @abc.abstractmethod
    def find_by_post_id(self, post_id) -> typing.List[Comment]:
        raise NotImplementedError()

    @abc.abstractmethod
    def delete(self, comment: Comment):
        raise NotImplementedError()
