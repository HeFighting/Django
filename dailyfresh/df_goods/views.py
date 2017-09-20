from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import JsonResponse
from df_goods.models import GoodsInfo, Goods, Image, BrowserHistory
from df_goods.enums import *

# Create your views here.


def test_tinymce(request):
    '''
    富文本显示
    '''
    goods = GoodsInfo.objects.get(id=1)
    return render(request, 'test_tinymce.html', {'goods': goods})


def home_list_page(request):
    '''
    显示主页
    '''
    # 1.获取每一个种类的3个新品信息和4个普通商品信息
    fruits_new = Goods.objects.get_goods_list_by_type(goods_type_id=FRUIT, limit=3, sort='new')
    fruits = Goods.objects_logic.get_goods_list_by_type(goods_type_id=FRUIT, limit=4)
    # 2.组织一个上下文
    context = {'fruits_new': fruits_new, 'fruits': fruits}
    return render(request, 'index.html', context)


# /goods/商品id/
def goods_detail(request, goods_id):
    '''
    显示商品的详情信息
    '''
    # 1.根据商品的id获取商品的信息
    goods = Goods.objects_logic.get_goods_by_id(goods_id=goods_id)
    # 2.获取获取商品的新品信息，两个
    goods_new_li = Goods.objects_logic.get_goods_list_by_type(goods_type_id=goods.goods_type_id, limit=2, sort='new')
    # 3.获取商品的种类标题
    type_title = GOODS_TYPE[goods.goods_type_id]
    # 4.记录用户浏览商品信息，如果用户没有登录，则不需要记录
    if request.session.has_key('is_login'):
        # 用户已登录
        passport_id = request.session.get('passport_id')
        # 往BrowserHistory对应的表中添加一条信息
        BrowserHistory.objects.add_one_history(passport_id=passport_id, goods_id=goods_id)
    return render(request, 'detail.html', {'goods': goods, 'goods_new_li': goods_new_li, 'type_title': type_title})


# /list/1/1/?sort=排序方式
def goods_list(request, goods_type_id, page_index):
    '''
    显示商品列表页信息
    '''
    # 0.获取排序方式sort
    sort = request.GET.get('sort', 'default')
    # 1.根据商品类型id获取商品信息
    goods_li = Goods.objects_logic.get_goods_list_by_type(goods_type_id=goods_type_id, sort=sort)
    # 2.进行分页
    paginater = Paginator(goods_li, 1)
    # 3.获取第pindex页的内容
    goods_li = paginater.page(page_index)  # goods_li是一个page对象
    # 4.获取页码列表
    pages = paginater.page_range
    # 5.todo:获取页码列表
    # 总页码数<=5
    # 如果当前页是前3页
    # 如果当前页是后3页
    # 既不是前3页也不是后3页 3 4 5 6 7
    # 5.1获取页码总数
    num_pages = paginater.num_pages
    # 5.2获取当前页页码
    current_num = int(page_index)
    if num_pages <= 5:
        pages = range(1, num_pages+1)
    elif current_num <= 3:
        pages = range(1, 6)
    elif num_pages - current_num <= 2:
        pages = range(num_pages-4, num_pages+1)
    else:
        pages = range(current_num-2, current_num+3)
    # 2.获取商品种类信息
    type_title = GOODS_TYPE[int(goods_type_id)]
    # 2.获取获取商品的新品信息，两个
    goods_new_li = Goods.objects_logic.get_goods_list_by_type(goods_type_id=goods_type_id, limit=2, sort='new')
    return render(request, 'list.html', {'goods_li': goods_li, 'type_title': type_title,
                                         'goods_new_li': goods_new_li, 'type_id': goods_type_id,
                                         'sort': sort, 'pages': pages})


def get_image_list(request):
    '''
    根据商品id列表获取图片信息
    '''
    # 1.获取goods_id_list信息
    goods_id_list = request.GET.get('goods_id_list')
    goods_id_list = goods_id_list.split(',')
    # 2.根据goods_id_list查询商品图片
    images = Image.objects.get_images_by_goods_id_list(goods_id_list=goods_id_list)
    # 3.组织json数据
    img_dict = {}
    for image in images:
        img_dict[image.goods_id] = image.img_url.name
    # 4.返回json数据
    return JsonResponse({'img_dict': img_dict})
























