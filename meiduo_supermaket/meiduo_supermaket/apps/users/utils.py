from django.contrib.auth.backends import ModelBackend
import re
from users.models import User


def get_user_by_account(account):
    """
    :param account:
    :return:
    """
    try:
        if re.match(r'^1[3-9]\d{9}$', account):
            user = User.objects.get(mobile=account)
        else:
            user = User.objects.get(username=account)
    except User.DoesNotExist:
        return None
    else:
        return user
class UsernameMobileBackend(ModelBackend):
    """ 自定义用户认证后端 """
    def authenticate(self, request, username=None, password=None, **kwargs):  # 函数重写
        """
        重写用户认证方法
        :param username:  账号或手机号
        :param password:  密码
        :param kwargs: 额外参数
        :return: user
        """
        # 查询
        user = get_user_by_account(username)
        # 校验
        if user and user.check_password(password):
            return user
        else:
            return None
        # 返回



