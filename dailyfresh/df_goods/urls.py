from django.conf.urls import url
from df_goods import views

urlpatterns = [
    url(r'^test_tinymce/$', views.test_tinymce),  # 富文本内容显示
    url(r'^$', views.home_list_page),  # 显示主页
    url(r'^goods/(\d+)/$', views.goods_detail),  # 显示商品详细信息
    url(r'list/(\d+)/(\d+)/$', views.goods_list),  # 显示商品列表页信息
    url(r'^get_image_list/$', views.get_image_list),  # 获取商品图片列表
]