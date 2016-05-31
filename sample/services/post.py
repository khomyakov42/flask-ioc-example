import typing
import inject
from datetime import datetime
from sample.models import Post, Comment
from sample.repository import PostRepository, CommentRepository, transaction


class PostService:
    post_repository = inject.attr(PostRepository)  # type: PostRepository
    comment_repository = inject.attr(CommentRepository)  # type: CommentRepository

    def create(self, author_name, title, text) -> Post:
        with transaction(self.post_repository):
            now = datetime.now()
            post = Post(None, author_name, title, text, now)
            self.post_repository.create(post)
            return post

    def comment_post(self, post: Post, author_name, text) -> Comment:
        with transaction(self.comment_repository):
            now = datetime.now()
            comment = Comment(None, post.id, author_name, text, now)
            self.comment_repository.create(comment)
            return comment

    def complain(self, post: Post):
        with transaction(self.post_repository, self.comment_repository):
            comments = self.comment_repository.find_by_post_id(post.id)
            for comment in comments:
                self.comment_repository.delete(comment)

            self.post_repository.delete(post)


