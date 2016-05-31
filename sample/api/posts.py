import inject
from flask.blueprints import Blueprint
from flask import request
from flask.ext.api.status import *
from sample.services import PostService
from sample.repository import PostRepository, CommentRepository

app = Blueprint('api.posts', __name__)
post_service = inject.instance(PostService)  # type: PostService
post_repository = inject.instance(PostRepository)  # type: PostRepository
comment_repository = inject.instance(CommentRepository)  # type: CommentRepository


def serialize_post(post):
    return dict(
        id=str(post.id),
        title=post.title,
        text=post.text,
        created_at=post.created_at.isoformat(),
        author_name=post.author_name
    )


def serialize_comment(comment):
    return dict(
        id=str(comment.id),
        text=comment.text,
        author_name=comment.author_name
    )


def serialize_post_with_comments(post, comments):
    data = serialize_post(post)
    data['comments'] = list(map(serialize_comment, comments))
    return data


@app.route('/posts', methods=['GET'])
def post_list():
    try:
        page = int(request.args.get('page', 0))
        if page < 0:
            raise ValueError()
    except ValueError:
        return {'error': 'bad_request'}, HTTP_400_BAD_REQUEST

    posts = post_repository.find_by_page(page, 20)
    return list(map(serialize_post, posts)), HTTP_200_OK


@app.route('/posts', methods=['POST'])
def create_post():
    try:
        data = dict(
            title=str(request.json['title'] or ''),
            text=str(request.json['text'] or ''),
            author_name=str(request.json['author_name'] or '')
        )
    except (ValueError, TypeError, IndexError):
        return {'error': 'bad_request'}, HTTP_400_BAD_REQUEST

    post = post_service.create(data['author_name'], data['title'], data['text'])
    return serialize_post(post), HTTP_201_CREATED


@app.route('/posts/<post_id>', methods=['GET'])
def get_post(post_id):
    post = post_repository.get(post_id)
    if post is None:
        return {'error': 'not_found'}, HTTP_404_NOT_FOUND

    comments = comment_repository.find_by_post_id(post.id)
    return serialize_post_with_comments(post, comments)


@app.route('/posts/<post_id>/comments', methods=['POST'])
def create_comment(post_id):
    post = post_repository.get(post_id)
    if post is None:
        return {'error': 'not_found', 'model': 'post'}, HTTP_400_BAD_REQUEST

    try:
        data = dict(
            author_name=str(request.json['author_name'] or ''),
            text=str(request.json['text'] or '')
        )
    except (ValueError, TypeError, IndexError):
        return {'error': 'bad_request'}, HTTP_400_BAD_REQUEST

    comment = post_service.comment_post(post, data['author_name'], data['text'])
    return serialize_comment(comment), HTTP_201_CREATED


