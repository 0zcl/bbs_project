from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from bbs import models
# Create your views here.
import queue,json,time

GLOBAL_MSG_QUEUES = {

}  # 队列：全局变量


def chat_dashboard(request):
    category_list = models.Category.objects.filter(set_to_top_menu=True).order_by("position_index")

    return render(request, "webchat/chat_index.html", {"category_list": category_list})


def send_msg(request):
    print(request.POST)
    msg_dic = request.POST.get("msg_dic")
    print(msg_dic, type(msg_dic))  # eg:{"from":"3","to":"2","type":"single","msg":"1111"} <class 'str'>
    if msg_dic:
        msg_dic = json.loads(msg_dic)
        print(msg_dic, type(msg_dic))  # {'type': 'single', 'from': '3', 'to': '1', 'msg': '3333'} <class 'dict'>
        print(">>接收到的消息", msg_dic["msg"])  # >>接收到的消息 3333
        queue_id = int(msg_dic["to"])  # 接收消息的用户id
        msg_dic["timestamp"] = time.time()  # 添加时间
        if msg_dic["type"] == "single":  # 一对一发送
            # 如果用户队列不存在, 注意，如果id(key)对应的队列不存在，则输出None,不会曝错
            if not GLOBAL_MSG_QUEUES.get(queue_id):
                GLOBAL_MSG_QUEUES[queue_id] = queue.Queue()  # 创建队列

            GLOBAL_MSG_QUEUES[queue_id].put(msg_dic)  # 将消息字典(带时间戳)放进队列
            print("全局队列>>:", GLOBAL_MSG_QUEUES)

    return HttpResponse("---receive msg---")


def get_new_msgs(request):  # 用户接收消息

    if request.user.userprofile.id not in GLOBAL_MSG_QUEUES:
        print("no queue for user [%s]" % request.user.userprofile.name)
        GLOBAL_MSG_QUEUES[request.user.userprofile.id] = queue.Queue()  # 创建队列

    q_obj = GLOBAL_MSG_QUEUES[request.user.userprofile.id]  # 队列对象
    msg_size = q_obj.qsize()  # 队列长度（即消息数量）
    msg_list = []
    if msg_size > 0:  # 有消息
        for msg in range(msg_size):
            msg_list.append(q_obj.get())  # 从队列取消息，即数据字典(先入先出)
        print(">>new msg:", msg_list)
    else:  # 没消息，要挂起
        # 超时挂起
        # 若队列为空，则60秒后会曝queue.Empty异常(相当在这60秒内卡住挂起)
        try:
            msg_list.append(q_obj.get(timeout=60))
        except queue.Empty:  # 若队列为空，则60秒后会曝queue.Empty异常(相当在这60秒内卡住挂起)
            print("\033[41;1mno msg for [%s][%s],timeout\033[0m" % (request.user.userprofile.id,request.user))
    print(">>>msg_list", msg_list)  # msg_list为消息列表，存放未接收的消息字典
    return HttpResponse(json.dumps(msg_list))  # 序列化，转化为json格式







