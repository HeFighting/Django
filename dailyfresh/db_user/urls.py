from django.conf.urls import url
from db_user import views

urlpatterns = [
    url(r'^register/$', views.register),  # 用户注册页面
    url(r'^is_name_valid/$', views.is_name_valid),  # 用户登陆校验
    url(r'^login/$', views.login),  # 显示登录页面
    url(r'^login_check/$', views.login_check),  # 显示登录页面
    url(r'^logout/$', views.logout),  # 退出登陆
    url(r'^address/$', views.address),  # 用户中心-地址页
    url(r'^$', views.user),  # 用户中心-个人信息页
    url(r'^order/$', views.order),  # 用户订单页面
]