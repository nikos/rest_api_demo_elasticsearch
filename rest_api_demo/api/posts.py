import logging

from flask import request
from flask_restplus import Resource

from rest_api_demo.api import api
from rest_api_demo.api import pagination_arguments
from rest_api_demo.api.serializers import blog_post, page_of_blog_posts
from rest_api_demo.posts import services
from rest_api_demo.posts.models import Post

log = logging.getLogger(__name__)

ns = api.namespace('blog/posts', description='Operations related to blog posts')


@ns.route('/')
class PostsCollection(Resource):
    @api.expect(pagination_arguments)
    @api.marshal_with(page_of_blog_posts)
    def get(self):
        """
        Returns list of blog posts.
        """
        args = pagination_arguments.parse_args(request)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)

        (entries, total) = services.get_blog_posts(page, per_page)
        return {
            'items': entries,
            'page': page,
            'per_page': per_page,
            'total': total
        }

    @api.expect(blog_post)
    def post(self):
        """
        Creates a new blog post.
        """
        services.create_blog_post(request.json)
        return None, 201


@ns.route('/<string:id>')
@api.response(404, 'Post not found.')
class PostItem(Resource):
    @api.marshal_with(blog_post)
    def get(self, id):
        """
        Returns a blog post.
        """
        return Post.get(id=id)

    @api.expect(blog_post)
    @api.response(204, 'Post successfully updated.')
    def put(self, id):
        """
        Updates a blog post.
        """
        data = request.json
        services.update_post(id, data)
        return None, 204

    @api.response(204, 'Post successfully deleted.')
    def delete(self, id):
        """
        Deletes blog post.
        """
        services.delete_post(id)
        return None, 204


@ns.route('/archive/<int:year>/')
@ns.route('/archive/<int:year>/<int:month>/')
@ns.route('/archive/<int:year>/<int:month>/<int:day>/')
class PostsArchiveCollection(Resource):
    @api.expect(pagination_arguments, validate=True)
    @api.marshal_with(page_of_blog_posts)
    def get(self, year, month=None, day=None):
        """
        Returns list of blog posts from a specified time period.
        """
        args = pagination_arguments.parse_args(request)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)

        start_month = month if month else 1
        end_month = month if month else 12
        start_day = day if day else 1
        end_day = day + 1 if day else 31
        start_date = '{0:04d}-{1:02d}-{2:02d}'.format(year, start_month, start_day)
        end_date = '{0:04d}-{1:02d}-{2:02d}'.format(year, end_month, end_day)

        (entries, total) = services.search_blogs_by_pubdate(start_date, end_date)

        return {
            'items': entries,
            'page': page,
            'per_page': per_page,
            'total': total
        }
