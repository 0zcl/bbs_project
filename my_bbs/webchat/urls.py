from django.conf.urls import url, include
from webchat import views

urlpatterns = [
    url(r'^$', views.chat_dashboard),
    url(r'^msg_send/$', views.send_msg, name="send_msg"),  # url不写动词
    url(r'^new_msgs/$', views.get_new_msgs, name="get_new_msgs"),  # 取消息
    url(r'^file_upload/$', views.webchat_file_upload, name="webchat_file_upload"),  # 上传文件(图片)
    url(r'^file_upload_size/$', views.get_file_upload_size, name="get_file_upload_size"),  # 获取后台接收文件的字节
    # 文件发送成功后将cache中key-value删除
    url(r'^cache_key_delete/$', views.delete_cache_key, name="delete_cache_key"),

]