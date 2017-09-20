from django.conf.urls import url
from df_cart import views


urlpatterns = [
    url(r'^add/$', views.cart_add),  # 添加商品信息到购物车
    url(r'^count/$', views.cart_count),  # 求出用户购物车中的商品总数
    url(r'^update/$', views.cart_update),  # 更新用户购物车中商品的数目
    url(r'^del/$', views.cart_del),  # 删除用户购物车中的信息
    url(r'^$', views.cart_show),  # 显示用户购物车页面
]