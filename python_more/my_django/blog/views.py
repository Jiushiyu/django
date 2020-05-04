# Create your views here.
from django.db.models import Count

from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

# 发送邮件
from django.core.mail import send_mail
# 可通过标签筛选文章
from taggit.models import Tag


# 用CBV类之前的post_list
def post_list(request, tag_slug=None):
    object_list = Post.publishedM.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    # 每页显示 3 篇文章
    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # 如果page参数不是一个整数就返回第一页
        posts = paginator.page(1)
    except EmptyPage:
        # 如果页数超过总页数就返回第一页
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page' : page, 'posts' : posts, 'tag': tag})

# 使用CBV类ListView 改写post_list视图
from django.views.generic import ListView
# 用于处理表单提交的数据
from .forms import EmailPostForm, CommentForm

# # CBV类
# class PostListView(ListView):
#     # 查询所有已发布的文章
#     queryset = Post.publishedM.all()
#     # 设置posts为模板变量的名称，如果不设置 默认是object_list
#     context_object_name = 'posts'
#     # 每页显示3篇文章
#     paginate_by = 3
#     # 指定需要渲染的模板，默认是blog/post_list.html
#     template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status="published",
                             publish__year=year, publish__month=month, publish__day=day)
    # 将处理评论表单功能整合在详情页
    # 列出文章对应的所有活动的评论
    comments = post.comments.filter(active=True)
    # 用于标记一个新评论是否被创建
    new_comment = None
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # 通过表单直接创建新数据对象，但是不要保存到数据库中
            # 表单对象的 save() 方法会返回一个由当前数据构成的，表单关联的数据类的对象，并且会将这个对象写入数据库。
            # 如果指定commit=False ，则数据对象会被创建但不会被写入数据库，便于在保存到数据库之前对对象进行一些操作。
            new_comment = comment_form.save(commit=False)
            # 设置外键为当前文章，明确了当前的评论是属于这篇文章的
            new_comment.post = post
            # 将评论数据对象写入数据库，save（）方法仅对ModelForm生效，因为Form类没有关联到任何数据模型
            new_comment.save()
    # 如果是get请求，则创建一个空白表单
    else:
        comment_form = CommentForm()
    # 显示相近Tag的文章
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_tags = Post.publishedM.filter(tags__in=post_tags_ids).exclude(id=post.id)
    # Count对每个文章tag计数，same_tags存放计数结果，降序排列，截取前四个结果
    similar_posts = similar_tags.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    return render(request, 'blog/post/detail.html',
                  {'post' : post, 'comments': comments, 'new_comment': new_comment, 'comments_form': comment_form,
                   'similar_posts': similar_posts})


# post_share视图
def post_share(request, post_id):
    # 通过id获取post对象
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == "POST":
        # 表单被提交
        form = EmailPostForm(request.POST)
        # 验证表单中的数据是否有效
        if form.is_valid():
            # 验证表单数据
            cd = form.cleaned_data
            # 发送邮件...
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) reconmmends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments:{}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'ysjwan007@163.com', [cd['to']])
            sent = True
    else:
        # 收到get请求，创建一个空白的form对象，填写之后通过post请求提交表单
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post':post, 'form': form, 'sent': sent})

