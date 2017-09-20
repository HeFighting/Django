# 定义celery任务
from celery import task
from django.core.mail import send_mail
from django.conf import settings

@task
def send_register_success_mail(email):
    '''
    用户注册成功后发送邮件
    '''
    msg = '<h1>欢迎你称为dailyfresh会员!<h1/>'
    send_mail('欢迎信息','',settings.EMAIL_FROM,[email,],html_message=msg)

