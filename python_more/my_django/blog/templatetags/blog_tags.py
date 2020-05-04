from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

register = template.Library()


# 自定义tag 显示总共多少
@register.simple_tag
def total_posts():
    return Post.publishedM.count()


# 自定义tag 显示最近三篇
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.publishedM.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


# 显示评论最多的文章
@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.publishedM.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]

# 过滤器
@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
