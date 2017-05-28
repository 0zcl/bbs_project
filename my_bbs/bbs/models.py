
from django.db import models
from django.contrib.auth.models import User  # django自带的用户表
# 要使界面出现错误提示，需导入ValidationError
from django.core.exceptions import ValidationError  # 合法性错误
import datetime

# Create your models here.


class Article(models.Model):  # 贴子表
    title = models.CharField(max_length=255)  # 标题
    brief = models.CharField(max_length=255, null=True, blank=True)  # 简要介绍
    # 贴子分类;这里需要加引号，因为程序从上往下走，还没有Category表呢，加引号则会通过反射自动去找Category表
    category = models.ForeignKey("Category")
    content = models.TextField(u"文章内容")
    author = models.ForeignKey("UserProfile")  # 作者
    pub_date = models.DateTimeField(blank=True, null=True)
    last_modify = models.DateTimeField(auto_now=True)  # 自动添加修改帖子时间
    priority = models.IntegerField(u"优先级", default=1000)  # 设置默认优先级为1000
    # upload_to表示图片存的目录；如果uploads目录不存在，会自动创建
    head_img = models.ImageField(u"文章标题图片", upload_to="uploads")

    status_choices = (("draft", u"草稿"),
                      ("published", u"已发布"),
                      ("hidden", u"隐藏"),
                      )
    publish_status = models.CharField(choices=status_choices, max_length=32, default="published")

    def clean(self):
        # Don't allow draft entries to have a pub_date.
        # 不允许草稿有发布日期
        if self.publish_status == 'draft' and self.pub_date is not None:
            raise ValidationError(u'Draft entries may not have a publication date.')
        # Set the pub_date for published items if it hasn't been set already.
        if self.publish_status == 'published' and self.pub_date is None:
            self.pub_date = datetime.date.today()

    def __str__(self):
        return self.title


class Comment(models.Model):  # 评论表
    article = models.ForeignKey(Article, verbose_name=u"所属文章")  # 评论所属的帖子
    # 父级评论
    parent_comment = models.ForeignKey("self", related_name="my_children", blank=True, null=True)  # 自关联
    comment_choices = ((1, u"评论"),
                       (2, u"点赞"),
                       )
    comment_type = models.SmallIntegerField(choices=comment_choices, default=1)  # 类型，默认为评论
    comment_user = models.ForeignKey("UserProfile")  # 评论者
    # 有个问题: 如果选择评论，但评论内容却可以为空，BUG
    comment = models.TextField(max_length=1024, blank=True, null=True)  # 点赞时评论为空
    comment_date = models.DateTimeField(auto_now_add=True)  # 评论时间

    def clean(self):
        # if self.comment_type == 1 and self.comment is None:
        if self.comment_type == 1 and len(self.comment) == 0:
            raise ValidationError(u"评论内容不能为空,SB")

    def __str__(self):
        return "C:%s;" % (self.comment)


class Category(models.Model):  # 版块(分类)表
    name = models.CharField(max_length=64, unique=True)  # 版块名
    brief = models.CharField(max_length=255, null=True, blank=True)  # 简要介绍
    set_to_top_menu = models.BooleanField(default=False)  # 是否显示在界面
    position_index = models.SmallIntegerField()  # 版块的位置
    admin = models.ManyToManyField("UserProfile", blank=True)  # 一个版块可有多个管理员，可不选择

    def __str__(self):
        return self.name


class UserProfile(models.Model):  # 用户表
    user = models.OneToOneField(User)  # 一对一关联，密码在User表
    name = models.CharField(max_length=64)
    signature = models.CharField(max_length=255, blank=True, null=True)  # 个人签名，可以为空
    head_img = models.ImageField(height_field=150, width_field=150, blank=True, null=True)  # 头像，可以不传
    # for web qq
    # 一个用户可以有多个好友(自关联), 可以为空
    # 你是我的好友，那我就是你的好友(django默认)，如:QQ ；你是我的粉丝，但我不是你是粉丝，可上openstack搜解决方案，如:webo
    friends = models.ManyToManyField("self", related_name="my_friends", blank=True)

    def __str__(self):
        return self.name

