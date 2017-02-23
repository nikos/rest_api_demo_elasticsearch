from rest_api_demo.posts.models import Post


def create_blog_post(data):
    title = data.get('title')
    body = data.get('body')
    categories = data.get('categories')
    post = Post(title=title, body=body, categories=categories)
    post.save()
    print("saved post: {}".format(post))


def update_post(id, data):
    post = Post.get(id=id)
    post.title = data.get('title')
    post.body = data.get('body')
    post.categories = data.get('categories')
    post.save()


def delete_post(post_id):
    post = Post.get(post_id)
    post.delete()


def get_categories():
    # TODO: search for all distinct categories used by all posts
    pass


def search_blogs_by_category(name):
    s = Post.search()
    s.query('match', categories=name)
    results = s.execute()
    for post in results:
        print(post.meta.score, post.title)
    return results
