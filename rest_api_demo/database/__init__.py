# from flask.ext.elasticsearch import FlaskElasticsearch
from elasticsearch_dsl.connections import connections

from rest_api_demo.posts.models import Post
from ..settings import ELASTICSEARCH_HOST

connections.create_connection(hosts=[ELASTICSEARCH_HOST], timeout=20)


# es = FlaskElasticsearch(app)

def init_db():
    # create the mappings in elasticsearch
    Post.init()


def reset_db():
    # db.drop_all()
    # db.create_all()
    pass
