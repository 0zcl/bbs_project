from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from bbs import models
# Create your views here.


def chat_dashboard(request):
    category_list = models.Category.objects.filter(set_to_top_menu=True).order_by("position_index")

    return render(request, "webchat/chat_index.html", {"category_list": category_list})

def send_msg(request):
    print(request.POST)
    print(">>接收到的消息", request.POST.get("msg"))
    return HttpResponse("---receive msg---")