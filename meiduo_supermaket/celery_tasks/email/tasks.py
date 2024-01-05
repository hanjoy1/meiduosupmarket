from django.core.mail import  send_mail
from django.conf import settings

def send_verify_email(to_email, verify_url):
    """定义发送验证邮件"""
    # 标题
    subject = "美多商城邮箱验证"
    # 发送内容:
    html_message = '<p>尊敬的用户您好！</p>' \
                   '<p>感谢您使用美多商城。</p>' \
                   '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                   '<p><a href="%s">%s<a></p>' % (to_email, verify_url, verify_url)
    send_mail(subject, '', settings.EMAIL_FROM, [], html_message)
    pass