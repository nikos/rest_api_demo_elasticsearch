# The examples in this file come from the Flask-SQLAlchemy documentation
# For more information take a look at:
# http://flask-sqlalchemy.pocoo.org/2.1/quickstart/#simple-relationships

from datetime import datetime
from elasticsearch_dsl import DocType, Date, String, Keyword, Text
from slugify import slugify


class Post(DocType):
    slug = String()  # deprecated: use Text or Keyword
    title = Text(analyzer='snowball', fields={'raw': Keyword()})
    body = Text(analyzer='snowball')
    pub_date = Date()
    created_date = Date()

    categories = Keyword()

    class Meta:
        index = 'blog'

    def save(self, ** kwargs):
        self.slug = slugify(self.title)
        self.created_date = datetime.now()
        return super(Post, self).save(** kwargs)

    def __repr__(self):
        return '<Post %r>' % self.title
