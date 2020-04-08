from django.urls import path, re_path
from django.conf.urls import include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from Test1.views import Test1List, Test1Detail, CustomAuthToken

urlpatterns = [
    #re_path(r'^test1prueba', CustomAuthToken.as_view()),
    re_path(r'^test1/', Test1List.as_view()),
    re_path(r'^test1/(?P<pk>\d+)$', Test1Detail.as_view()),
]