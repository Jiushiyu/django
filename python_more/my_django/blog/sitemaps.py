from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap):
    # changefreq 和 priority 属性表示文章页面更新的频率和这些文章与站点的相关性（最大相关性为1）
    changefreq = 'weekly'
    priority = 0.9

    # Django默认会调用数据对象的 get_absolute_url() 获取对应的URL，
    # 如果想手工指定具体的URL，可以为PostSitemap 添加一个 location 方法
    def items(self):
        return Post.publishedM.all()

    # 接收 items() 返回的每一个数据对象然后返回其更新时间
    def lastmod(self, obj):
        return obj.updated
