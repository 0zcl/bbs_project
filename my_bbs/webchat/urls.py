from django.conf.urls import url, include
from webchat import views

urlpatterns = [
    url(r'^$', views.chat_dashboard),

]