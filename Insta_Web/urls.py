"""Insta_Web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from .views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home/$', Home.as_view(), name='home'),
    url(r'^start_unfollow/$', Unfollow.as_view(), name='start_unfollow'),
    url(r'^stop_unfollow/$', Unfollow.as_view(), name='stop_unfollow'),
    url(r'^delete_message/$', DeleteMessageFunctionality.as_view(), name='delete_message'),
    url(r'^play_message/$', PlayMessageFunctionality.as_view(), name='play_message'),
    url(r'^pause_message/$', PauseMessageFunctionality.as_view(), name='pause_message'),
    url(r'^send_message/$', MessageFunctionality.as_view(), name='send_message'),
    url(r'^like_play/$', PlayLikesFunctionality.as_view(), name='likes_play'),
    url(r'^like_pause/$', PauseFunctionality.as_view(), name='like_pause'),
    url(r'^play/$', PlayFunctionality.as_view(), name='play'),
    url(r'^pause/$', PauseFunctionality.as_view(), name='pause'),
    url(r'delete/$', DeleteFunctionality.as_view(), name='delete'),
    url(r'^dashboard_functions/$', InstagramFunctions.as_view(), name='dashboard_functions'),
    url(r'^dashboard/(?P<username>\w+)/$', Dashboard.as_view(), name='dashboard'),
    url(r'^login/$', Login.as_view(), name='login'),
    url(r'^logout/$', Logout.as_view(), name='logout'),
    url(r'^signup/$', SignUp.as_view(), name='signup'),
    url(r'^$', HomePage.as_view(), name='index'),
]
