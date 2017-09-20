from django.shortcuts import render
from utils.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_GET,require_POST,require_http_methods
from df_goods.models import Goods
from df_cart.models import Cart
# Create your views here.

@require_GET
@login_required
def cart_add(request):
    '''
    添加购物车信息
    '''
    # 1.接收商品id和商品数目
    goods_id = request.GET.get('goods_id')
    goods_count = request.GET.get('goods_count')
    # 2.获取登录用户的passport_id
    passport_id = request.session.get('passport_id')
    # 3.添加商品信息到购物车
    # 3.1判断商品库存是否充足
    goods = Goods.objects.get_goods_by_id(goods_id=goods_id)
    if goods.goods_stock < int(goods_count):
        # 商品库存不足
        return JsonResponse({'res': 0})
    else:
        # 商品库存不足
        # 添加商品信息到购物车
        Cart.objects.add_one_cart_info(passport_id=passport_id, goods_id=goods_id, goods_count=int(goods_count))
        return JsonResponse({'res': 1})


@require_GET
@login_required
def cart_count(request):
    '''
    获取用户购物车中商品的数目
    '''
    # 1.获取用户的passport_id
    passport_id = request.session.get('passport_id')
    # 2.根据passport_id查询用户购物车中的信息
    res = Cart.objects.get_cart_count_by_passport(passport_id=passport_id)
    # 3.返回json数据
    return JsonResponse({'res': res})


@login_required
def cart_show(request):
    '''
    显示用户的购物车页面
    '''
    # 1.获取用户的passport_id
    passport_id = request.session.get('passport_id')
    # 2.根据passport_id查询购物车信息
    cart_list = Cart.objects_logic.get_cart_list_by_passport(passport_id=passport_id)
    return render(request, 'cart.html', {'cart_list': cart_list})

@require_GET
@login_required
def cart_update(request):
    '''
    更新用户购物车中商品的数目
    '''
    # 1.接收商品的id和商品的数目
    goods_id = request.GET.get('goods_id')
    goods_count = request.GET.get('goods_count')
    passport_id = request.session.get('passport_id')
    # 2.更新用户购物车中对应商品的信息
    update_res = Cart.objects.update_cart_info_by_passport(passport_id=passport_id,
                                                           goods_id=goods_id,
                                                           goods_count=int(goods_count))
    # 3.根据update_res返回json数据
    if update_res:
        # 更新成功
        return JsonResponse({'res': 1})
    else:
        # 更新失败
        return JsonResponse({'res': 0})


@require_GET
@login_required
def cart_del(request):
    '''
    删除购物车信息
    '''
    # 1.获取购物车信息的id
    cart_id = request.GET.get('cart_id')
    try:
        # 2.根据id删除购物车记录信息
        cart_info = Cart.objects.get_one_cart_info_by_id(cart_id=cart_id)
        # 进行删除
        cart_info.delete()
        # 3.返回json数据
        return JsonResponse({'res': 0})
    except:
        return JsonResponse({'res': 1})


























