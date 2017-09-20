from django.shortcuts import render, redirect
from db_user.models import Passport,Address
from df_order.models import OrderBasic
from django.http import HttpResponseNotAllowed,JsonResponse
from django.views.decorators.http import require_GET,require_POST,require_http_methods
from django.core.mail import send_mail #导入发送邮件的函数
from django.conf import settings
from db_user.tasks import send_register_success_mail
import time
from datetime import datetime,timedelta
from utils.decorators import login_required
from df_goods.models import BrowserHistory

# Create your views here.


# ==========================================登陆注册页面=============================================
@require_http_methods(['GET', 'POST'])
def register(request):
    '''
    显示注册界面
    '''
    if request.method == 'GET':
        # 显示用户注册页面
        return render(request, 'register.html')
    elif request.method == 'POST':
        # 处理用户注册信息
        # 1.获取用户注册信息
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        # 2.将获取的数据保存进数据库
        '''
        p = Passport()
        p.username = username
        p.password = password
        p.email = email
        p.save()
        '''
        Passport.objects.add_one_passport(username=username, password=password, email=email)
        # msg = '<h1>欢迎你称为dailyfresh会员!<h1/>'
        # send_mail('欢迎信息','',settings.EMAIL_FROM,[email,],html_message=msg)
        send_register_success_mail.delay(email) # 需要调用delay函数
        # 3.跳转到登陆页面
        return redirect('/')


'''
@require_POST
def register_handle(request):
    # 处理用户注册信息
    # 1.获取用户注册信息
    username = request.POST.get('user_name')
    password = request.POST.get('pwd')
    email = request.POST.get('email')
    # 2.将获取的数据保存进数据库
    p = Passport()
    p.username = username
    p.password = password
    p.email = email
    p.save()
    # 3.跳转到登陆页面
    return redirect('/')
'''


def is_name_valid(request):
    '''
    验证用户名是否存在
    '''
    username = request.POST.get('user_name')
    passport = Passport.objects.get_one_passport(username=username)
    if passport:
        res = 0
    else:
        res = 1
    return JsonResponse({"res": res})


# /user/login/
def login(request):
    '''
    显示登录页面
    '''
    # 1.判断是否存在username cookie信息
    if 'username' in request.COOKIES:
        username = request.COOKIES['username']
    else:
        username = ''
    return render(request, 'login.html', {'username': username})


@require_POST
def login_check(request):
    '''
    进行用户的登陆校验
    '''
    # 1.获取用户输入的用户名和密码
    username = request.POST.get('username')
    print(username)
    password = request.POST.get('password')
    print(password)
    # 2.根据用户名和密码查询账户信息
    passport = Passport.objects.get_one_passport(username=username, password=password)
    print(passport)
    # 3.根据返回值返回json数据
    if passport:
        # 获取用户之前访问的url地址
        # if request.session.has_key('pre_url_path'):
        #     next = request.session.get('pre_url_path')
        # else:
        #     next = '/'
        next = request.session.get('pre_url_path', '/')
        # 用户名密码正确
        jres = JsonResponse({'res': 1, 'next':next})
        # 4.是否需要记住用户名
        remember = request.POST.get('remember')
        print(type(remember))
        if remember == 'true':
            # 记住用户名，使用cookie
            jres.set_cookie('username', username, expires=datetime.now()+timedelta(days=14))
        # 5.记录用户的登录状态
        request.session['is_login'] = True
        request.session['passport_id'] = passport.id
        request.session['username'] = username
        return jres
    else:
        # 用户名或密码错误
        return JsonResponse({'res': 0})


def logout(request):
    '''
    退出登录状态
    '''
    # 1.清空记录的登录状态
    request.session.flush()
    # 2.跳转回登录主页
    return redirect('/')

# ======================================用户中心===========================================


@require_http_methods(['GET', 'POST'])
@login_required
def address(request):
    '''
    用户中心地址页面
    '''
    # 获取登陆账户的id
    passport_id = request.session['passport_id']
    if request.method == 'POST':
        # 添加收货地址信息
        # 1.获取用户输入的地址信息
        recipient_name = request.POST.get('uname')
        recipient_addr = request.POST.get('addr')
        zip_code = request.POST.get('zip_code')
        recipient_phone = request.POST.get('phone')
        # 2.添加收货地址信息
        Address.objects.add_one_address(passport_id=passport_id, recipient_name=recipient_name,
                                        recipient_addr=recipient_addr, zip_code=zip_code,
                                        recipient_phone=recipient_phone)
    # 3.根据passport_id查询账户的默认收货地址
    addr = Address.objects.get_default_address(passport_id=passport_id)
    # 4.使用模版并传数据,并刷新页面
    return render(request, 'user_center_site.html', {'addr': addr, 'page':'addr'})


@login_required
def user(request):
    '''
    用户中心-个人信息页
    '''
    # 1.获取登陆账户的id
    passport_id = request.session['passport_id']
    # 2.根据passport_id查询账户的默认收货地址
    addr = Address.objects.get_default_address(passport_id=passport_id)
    # 3.获取用户的最近浏览信息
    browse_li = BrowserHistory.objects_logic.get_browse_list_by_passport(passport_id=passport_id)
    # 4.给模版传递数据
    return render(request, 'user_center_info.html', {'addr': addr, 'page': 'user', 'browse_li': browse_li})


@login_required
def order(request):
    '''
    用户订单页面
    '''
    passport_id = request.session.get('passport_id')
#     # 1.查询用户订单信息
    order_basic_list = OrderBasic.objects_logic.get_order_basic_list_by_passport(passport_id=passport_id)
    return render(request, 'user_center_order.html', {'page': 'addr',
                                                      'order_basic_list': order_basic_list})












