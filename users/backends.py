# -*- coding: utf-8 -*-
# @Time    : 2019-05-22 15:47
# @Author  : chunquansang
# @FileName: backends.py
# @Software: PyCharm

from users.models import User

class EmailBackend(object):
    def authenticate(self, request, **credentials):
        email = credentials.get('email', credentials.get('username'))
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            pass
        else:
            if user.check_password(credentials["password"]):
                return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
