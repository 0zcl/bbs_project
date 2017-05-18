
from django.forms import ModelForm
from bbs import models


class ArticleModelForm(ModelForm):

    class Meta:
        model = models.Article
        exclude = ("author", "pub_date", "priority")

    # 重构modelform的初始化类的方式；前面已经继承modelform，下面进行重构
    def __init__(self, *args, **kwargs):
        super(ArticleModelForm, self).__init__(*args, **kwargs)
        # self.fields["field_name"].widget.attrs({"class":"form-control"})  # 只给某字段加样式

        for field_name in self.base_fields:
            field = self.base_fields[field_name]  # 循环取出所有字段
            field.widget.attrs.update({"class": "form-control"})  # 给字段加上样式


