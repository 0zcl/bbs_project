
# 自定义中间件，供学习中间件
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse


class MyCustomMiddleWare(MiddlewareMixin):

    def process_request(self, request):
        # 如果返回None, Django将继续处理这个request, 执行后续的中间件， 然后调用相应的view.
        print("----in process request----")
        # request.user是一个对象: uber <class 'django.utils.functional.SimpleLazyObject'>
        print(request.user, type(request.user))
        #　可以做权限控制!!!方便，不用像之前专门用permission模块来写
        # if request.user == "uber":
        if request.user.username == "uber":
            print("uber no permission")
            # 如果返回HttpResponse对象, Django将不再执行任何其它的中间件(而无视其种类)以及相应的view。
            # Django将立即返回该HttpResponse
            return HttpResponse("uber no permission")
        else:
            print("haha")


    def process_view(self, request, view_func, view_args, view_kwargs):
        # 这个方法的调用时机在Django执行完request预处理函数并确定待执行的view之后，但在view函数实际执行之前。
        print("----in process view----")
        print("request>>>", request)
        print("view_func>>>", view_func)
        print("view_args>>>", view_args)
        print("view_kwargs>>>", view_kwargs)

    def process_response(self, request, response):
        # 这个方法的调用时机在Django执行view函数并生成response之后
        print("----in process response----")
        # 不同可能返回None的request和view预处理函数, process_response()必须返回HttpResponse对象.
        # 这个response对象可以是传入函数的那一个原始对象(通常已被修改)，也可以是全新生成的
        return response



    def process_exception(self, request, exception):
        print("----come to exception----")
        print("exception>>>", exception)


# 访问结果如下
"""
[25/Jun/2017 15:15:11] "GET /webchat/new_msgs/ HTTP/1.1" 500 14623
----in process request----
----in process view----
request>>> <WSGIRequest: GET '/bbs/category/2/'>
view_func>>> <function category at 0x000000000426E950>
view_args>>> ('2',)
view_kwargs>>> {}
>>>>找到最新文章的ID 29
----in process response----
"""


#　当访问/bbs/category/55/时出错(category的id没有55那么大)，结果如下(未走到view方法)
#　如果在view方法里抛出导演raise xxxexception. 则能走到view方法，后再调用process_exception
"""
[25/Jun/2017 15:17:47] "GET /bbs/latest_article_id/?latest_id=29 HTTP/1.1" 200 24
----in process request----
----in process view----
request>>> <WSGIRequest: GET '/bbs/category/55/'>
view_func>>> <function category at 0x000000000444E950>
view_args>>> ('55',)
view_kwargs>>> {}
----come to exception----
exception>>> Category matching query does not exist.
Internal Server Error: /bbs/category/55/
"""

