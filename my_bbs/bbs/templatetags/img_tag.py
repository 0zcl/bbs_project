from django import template
from django.utils.html import format_html

register = template.Library()


@register.filter  # 注册
def truncate_url(img_url):  # 截断url
    # print(">>>>", img_url.name)  # uploads/20141224_162507.jpg
    # print(">>>>", img_url.name.split("/", maxsplit=1)[1])  # 20150225_161922.jpg
    return img_url.name.split("/", maxsplit=1)[-1]


@register.simple_tag
def filter_comment(article_obj):
    query_set = article_obj.comment_set.select_related()  # 反向关联查询(包含评论与点赞)
    comments = {
        "comment_count": query_set.filter(comment_type=1).count(),  # 评论数
        "thumb_count": query_set.filter(comment_type=2).count(),  # 点赞数
    }
    return comments  # 后端返回给前端是一个字典
