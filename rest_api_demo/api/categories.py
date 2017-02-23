import logging

from flask_restplus import Resource

from rest_api_demo.api import api
from rest_api_demo.api.serializers import category, category_with_posts
from rest_api_demo.posts.services import get_categories, search_blogs_by_category

log = logging.getLogger(__name__)

ns = api.namespace('blog/categories', description='Operations related to blog categories')


@ns.route('/')
class CategoryCollection(Resource):

    @api.marshal_list_with(category)
    def get(self):
        """
        Returns list of blog categories.
        """
        return get_categories()


@ns.route('/<string:name>')
@api.response(404, 'Category not found.')
class CategoryItem(Resource):

    @api.marshal_with(category_with_posts)
    def get(self, name):
        """
        Returns a category with a list of posts.
        """
        return search_blogs_by_category(name)
