from django.conf.urls import url, include
from webchat import views

urlpatterns = [
    url(r'^$', views.chat_dashboard),
    url(r'^msg_send/$', views.send_msg, name="send_msg"),  # url不写动词
    url(r'^new_msgs/$', views.get_new_msgs, name="get_new_msgs"),  # 取消息
    url(r'^file_upload/$', views.webchat_file_upload, name="webchat_file_upload"),  # 上传文件(图片)

]