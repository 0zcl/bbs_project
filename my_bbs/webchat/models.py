from django.db import models
from bbs.models import UserProfile
# Create your models here.

# 群聊的表
class WebGroup(models.Model):
    name = models.CharField(max_length=64)  # 群名
    brief = models.CharField(max_length=255, blank=True)  # 群介绍，可为空
    owner = models.ForeignKey(UserProfile)  # 群主
    # 下面这句代码如果再加上null=True,会曝错
    # webchat.WebGroup.admins: (fields.W340) null has no effect on ManyToManyField.
    admins = models.ManyToManyField(UserProfile, blank=True, related_name="group_admins")
    # 'WebGroup.admins' clashes with reverse accessor for 'WebGroup.members'.
    # HINT: Add or change a related_name argument to the definition for 'WebGroup.admins' or 'WebGroup.members'.
    # 只要涉及到同一张表的多个字段关联同一张表，就需要加个related_name
    members = models.ManyToManyField(UserProfile, blank=True, related_name="group_members")  # 群成员
    max_members = models.IntegerField(default=200)  # 默认最大群人数为200

    def __str__(self):
        return self.name