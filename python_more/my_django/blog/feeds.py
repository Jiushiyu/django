from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post


class LatestPostFeed(Feed):
    title = 'My blog'
    link = '/blog/'
    description = 'New posts of my blog.'

    def items(self):
        return Post.publishedM.all()[:5]

    def item_title(self, item):
        return item.title

    # item_description 没有对post.body进行处理，所以返回未经处理的Markdown代码
    def item_description(self, item):
        return truncatewords(item.body, 30)

