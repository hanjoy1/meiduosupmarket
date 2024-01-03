from django.shortcuts import render
from django.views import View
from verifications.libs.captcha.captcha import captcha
from django_redis import get_redis_connection
from django.http import HttpResponse
from . import constants
# Create your views here.


class ImageCodeView(View):
    """图形验证码"""
    def get(self, request, uuid):
        # uuid : 通用图形验证码
        # return image/jpg
        # 接受参数校验参数
        # 实现主体业务逻辑 生成，保存，响应图形验证码
        text, image = captcha.generate_captcha()
        # 保存验证码
        redis_conn = get_redis_connection('verify_code')
        #redis_conn.setex('key', 'expires', 'value')
        redis_conn.setex('img_%s' % uuid, constants.IMAGE_CODE_REDIS_EXPIRES, text)
        # 响应验证码
        return HttpResponse(image, content_type='image/jpg')



