from bbs import models
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required  #导入django自带的登陆装饰器
from django.contrib.auth import authenticate,login,logout  #login用于登陆跳转
from bbs import handle_comment
from bbs import forms
import datetime,json

# Create your views here.


category_list = models.Category.objects.filter(set_to_top_menu=True).order_by("position_index")


def acc_login(request):
    if request.method == "POST":
        user = authenticate(username=request.POST.get("username"),
                            password=request.POST.get("password"))
        if user is not None:
            login(request, user)  # 登陆成功后保存session
            print(">>>>>>login success>>>>>")
            # 获取登陆后需要跳转到的url
            return HttpResponseRedirect(request.GET.get("next") or "/bbs")
        else:
            # 返回错误信息给前端
            login_error = "Wrong username or password!"
            return render(request, "bbs/login.html", {"login_error": login_error})

    return render(request, 'bbs/login.html')


def acc_logout(request):
    logout(request)  # 退出登陆　应该有清除session
    return HttpResponseRedirect('/bbs')


def index(request):
    article_list = models.Article.objects.filter(publish_status="published")
    category_obj = models.Category.objects.get(position_index=1)
    return render(request, "bbs/index.html", {"category_list": category_list,
                                              "article_list": article_list,
                                              "category_obj": category_obj})


def category(request, category_id):
    category_obj = models.Category.objects.get(id=category_id)
    if category_obj.position_index == 1:  # 用户访问首页
        article_list = models.Article.objects.filter(publish_status="published")
    else:
        article_list = models.Article.objects.filter(category=category_id, publish_status="published")
    return render(request, "bbs/index.html", {"category_list": category_list,
                                              "category_obj": category_obj,
                                              "article_list": article_list})


def article_detail(request, article_id):
    article_obj = models.Article.objects.get(id=article_id)
    # 通过反向关联取出当前文章的所有评论，再调用build_tree方法，处理文章评论的树结构
    comment_tree = handle_comment.build_tree(article_obj.comment_set.select_related())
    return render(request, "bbs/article_detail.html", {"article_obj": article_obj,
                                                       "category_list": category_list})


def comment(request):
    print(">>>>>", request.POST)
    # 创建评论
    if request.method == "POST":
        new_comment_obj = models.Comment(
            article_id = request.POST.get("article_id"),
            comment_type = request.POST.get("comment_type"),
            parent_comment_id = request.POST.get("parent_comment") or None,
            comment_user_id = request.user.userprofile.id,
            comment = request.POST.get("comment_content")
        )
        new_comment_obj.save()  # 保存到数据库
        return HttpResponse("post-comment-success")


def get_comments(request, article_id):
    article_obj = models.Article.objects.get(id=article_id)
    comment_tree = handle_comment.build_tree(article_obj.comment_set.select_related())
    render_comment = handle_comment.render_comment_tree(comment_tree)  # render_comment为含html字符串
    return HttpResponse(render_comment)


def new_article(request):
    if request.method == "GET":
        article_form = forms.ArticleModelForm

        return render(request, "bbs/new_article.html", {"article_form": article_form,
                                                        "category_list": category_list})
    elif request.method == "POST":

        # 如果想通过django往后台传图片，需加参数request.FILES.(传图片的参数)
        article_form = forms.ArticleModelForm(request.POST, request.FILES)
        if article_form.is_valid():
            # print(">>>>", article_form.cleaned_data)  # 字典形式，把作者ID加上去
            # 下面这句其实无法添加数据，不信你可以打印看看
            # article_form.cleaned_data["author_id"] = request.user.userprofile.id
            article_data = article_form.cleaned_data
            article_data["author_id"] = request.user.userprofile.id
            article_data["pub_date"] = datetime.date.today()

            # 创建文章
            article_obj = models.Article(**article_data)
            article_obj.save()
            return render(request, "bbs/new_article.html", {"article_form": article_form,
                                                            "category_list": category_list})

        else:
            return render(request, "bbs/new_article.html", {"article_form": article_form,
                                                            "category_list": category_list})


def file_upload(request):
    # 上传文件
    print(request.FILES)
    # >>> data.rsd <class 'django.core.files.uploadedfile.TemporaryUploadedFile'>
    print(">>>", request.FILES.get("filename"), type(request.FILES.get("filename")))
    # file_obj是一个文件名柄,django保存上传文件的句柄
    file_obj = request.FILES.get("filename")
    # uploads目录下原本没有file_obj.name文件，这里临上传的文件复制到uploads目录下
    with open('uploads/%s' % file_obj.name, 'wb+') as destination:
        for chunk in file_obj.chunks():  # chunks方法是django封装好的
            destination.write(chunk)

    return render(request, "bbs/new_article.html", {"category_list": category_list})


def get_latest_article_id(request):
    latest_article_id = request.GET.get("latest_id")
    if latest_article_id:
        new_article_count = models.Article.objects.filter(id__gt=latest_article_id).count()
        print(">>>>", new_article_count, type(new_article_count))
    else:  # 如果当前页面没有文章，则latest_article_id为空
        new_article_count = 0
        print(">>页面无文章")

    return HttpResponse(json.dumps({'new_article_count': new_article_count}))




