# coding=utf-8
__author__ = 'bibi'
__date__ = '2018/1/29 17:11'


from random import Random
from django.core.mail import send_mail


from user.models import EmailVerifyRecord
from Mxonline.settings import EMAIL_FROM


def generate_random_str(randomlength):
    str = ''
    char = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    length = len(char) - 1
    random = Random()
    for i in range(randomlength):
        str+=char[random.randint(0,length)]
    return str


def send_register_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    email_record.code = generate_random_str(16)
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ''
    email_body = ''

    if send_type =='register':
        email_title = 'Mxonline注册激活链接'
        email_body = '请点击以下链接激活你的账号：http://127.0.0.1:8000/active/{0}'.format(email_record.code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            print('ss')

    if send_type=='forget':
        email_title = 'Mxonline密码重置链接'
        email_body = '请点击以下链接修改你的密码：http://127.0.0.1:8000/reset/{0}'.format(email_record.code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            print('ss')