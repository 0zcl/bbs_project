from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from bbs import models
# Create your views here.
import queue,json,time
from webchat import models as chat_models
from django.core.cache import cache

GLOBAL_MSG_QUEUES = {

}  # 队列：全局变量


def chat_dashboard(request):
    category_list = models.Category.objects.filter(set_to_top_menu=True).order_by("position_index")

    return render(request, "webchat/chat_index.html", {"category_list": category_list})


def send_msg(request):
    print("request.POST", request.POST)
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
        else:  # 群发，则将消息字典(带时间戳)群成员各自的队列
            # print("群发消息")
            group_obj = chat_models.WebGroup.objects.get(id=queue_id)  # 群组对象
            members = group_obj.members.select_related()
            # print(">>群组成员:", members)
            for member in members:
                print(member.name, member.id)
                # 如果用户队列不存在, 注意，如果id(key)对应的队列不存在，则输出None,不会曝错
                if not GLOBAL_MSG_QUEUES.get(member.id):
                    GLOBAL_MSG_QUEUES[member.id] = queue.Queue()  # 创建队列
                if member.id != request.user.userprofile.id:
                    GLOBAL_MSG_QUEUES[member.id].put(msg_dic)  # 将消息字典(带时间戳)群成员各自的队列

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


def webchat_file_upload(request):  # 处理聊天室上传文件/图片
    print(">>web_chat_upload_file")
    if request.method == "POST":
        # print("request.POST", request.POST)  # <QueryDict: {}>
        # <MultiValueDict: {'file': [<InMemoryUploadedFile: 213915683426.jpg (image/jpeg)>]}>,PS:"file"是在前端定义的
        print("request.FILES", request.FILES)
        # file_obj是一个文件名柄,django保存上传文件的句柄
        # typeof(file_obj): <class 'django.core.files.uploadedfile.InMemoryUploadedFile'>
        file_obj = request.FILES.get("file")  # (输出)print(file_obj): 213915683426.jpg
        recv_filesize = 0
        # uploads目录下原本没有file_obj.name文件，这里临上传的文件复制到uploads目录下
        with open('uploads/webchat/%s' % file_obj.name, 'wb+') as destination:  # 如果上传相同文件会覆盖，功能待改善
            for chunk in file_obj.chunks():  # chunks方法是django封装好的
                destination.write(chunk)

                recv_filesize += len(chunk)
                cache.set(file_obj, recv_filesize)  # 存入缓存
        # 前端通过定时器发起请求，请求recv_filesize，如何能让这个请求也能接收到局部变量recv_filesize??
        # 方法一: 可设置全局字典，{"filename": recv_filesize}
        # 方法二: django自带缓存系统cache,临时保存数据
        print("接收到文件的大小:", recv_filesize)
        return HttpResponse("upload file success")


def get_file_upload_size(request):  # 获取后台接收文件的字节
    # print("request.GET>>:", request.GET)  # <QueryDict: {'filename': ['jack.rar']}>
    filename = request.GET.get("filename")
    progress = cache.get(filename)  # 从缓存中取出服务端已接收的字节数
    print("file[%s] uploading progress[%s]" % (filename, progress))

    return HttpResponse(json.dumps({"recv_size": progress}))


def delete_cache_key(request):
    print("delete_cache_key", request.GET.get("cache_key"))
    cache.delete(request.GET.get("cache_key"))

    return HttpResponse("delete_success")