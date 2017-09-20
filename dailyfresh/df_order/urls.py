from django.conf.urls import url
from df_order import views

urlpatterns = [
    url(r'^$', views.order_place),  # 显示订单提交页面
    url(r'^commit/$', views.order_commit),  # 订单生成
]