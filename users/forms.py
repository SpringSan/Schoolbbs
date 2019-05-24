# -*- coding: utf-8 -*-
# @Time    : 2019-05-22 15:35
# @Author  : chunquansang
# @FileName: forms.py
# @Software: PyCharm

from users.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "student_num", "major", "qq_num")