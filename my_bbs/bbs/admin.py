from django.contrib import admin
from bbs import models
# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "brief", "category", "content", "author",
                    "pub_date", "last_modify", "priority", "publish_status")


class CommentAdmin(admin.ModelAdmin):
    list_display = ("article", "parent_comment", "comment_type",
                    "comment", "comment_user", "comment_date")


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "set_to_top_menu")


admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Comment, CommentAdmin)
admin.site.register(models.UserProfile)
