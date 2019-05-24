# -*- coding: utf-8 -*-
# @Time    : 2019-05-22 17:10
# @Author  : chunquansang
# @FileName: forms.py
# @Software: PyCharm
from django import forms
from comments.models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
