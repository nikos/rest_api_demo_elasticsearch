from elasticsearch_dsl import A, Search

from rest_api_demo.posts.models import Post


def get_blog_posts(page, per_page):
    s = Post.search()
    s = s[(page - 1) * per_page:page * per_page]  # pagination {"from": 10, "size": 10}
    response = s.execute()
    return _convert_results(response)


def create_blog_post(data):
    title = data.get('title')
    body = data.get('body')
    categories = data.get('categories')
    post = Post(title=title, body=body, categories=categories)
    post.save()
    print("saved post: {}".format(post))


def _convert_results(response):
    entries = []
    for post in response:
        # TODO: Could also expose score (via: post.meta.score)
        entry = post.to_dict()
        entry['id'] = post.meta.id
        entries.append(entry)

    return entries, response.hits.total


def search_blogs_by_pubdate(start_date, end_date):
    s = Post.search()
    s = s.query('range', pub_date={'gte': start_date, 'lte': end_date})
    response = s.execute()
    return _convert_results(response)


def search_blogs_by_category(name):
    s = Post.search()
    s = s.query('match', categories=name)  # vs. term
    response = s.execute()
    (posts, total) = _convert_results(response)
    return {'name': name, 'posts': posts}


def update_post(id, data):
    post = Post.get(id=id)
    post.title = data.get('title')
    post.body = data.get('body')
    post.categories = data.get('categories')
    post.save()


def delete_post(post_id):
    post = Post.get(id=post_id)
    post.delete()


def get_categories():
    # search for all distinct categories used by all posts
    a = A('terms', field='categories')
    s = Search()
    s = s[0:0]  # we are only interested in term distribution, not real results
    s.aggs.bucket('category_terms', a)
    response = s.execute()

    categories = []
    for item in response.aggregations.category_terms.buckets:
        # print('{} {}'.format(item.key, item.doc_count))
        categories.append({'name': item.key})

    return categories
