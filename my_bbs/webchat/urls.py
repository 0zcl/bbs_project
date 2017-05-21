from django.conf.urls import url, include
from webchat import views

urlpatterns = [
    url(r'^$', views.chat_dashboard),
    url(r'^msg_send/$', views.send_msg, name="send_msg"),  # url不写动词
]