# -*- coding: utf-8 -*-
# @Time    : 2019-05-22 15:32
# @Author  : chunquansang
# @FileName: urls.py
# @Software: PyCharm

from django.conf.urls import url
from users import views

app_name = "users"
urlpatterns = [
    url(r'^register/', views.register, name='register'),

]