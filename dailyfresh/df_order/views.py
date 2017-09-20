from django.shortcuts import render
from django.views.decorators.http import require_http_methods,require_POST,require_GET
from django.db import transaction  # 导入事务包
from utils.decorators import login_required
from django.http import JsonResponse
from db_user.models import Address
from df_order.models import OrderBasic,OrderDetail
from df_cart.models import Cart
from datetime import datetime
# Create your views here.

@require_POST
@login_required
def order_place(request):
    '''
    订单提交页面
    '''
    passport_id = request.session.get('passport_id')
    # 1.查询用户的默认收货地址
    addr = Address.objects.get_default_address(passport_id=passport_id)
    # 2.获取用户的购买的商品信息
    cart_id_list = request.POST.getlist('cart_id_list')  # [1,2,3]
    # 3.根据cart_id_list查询购物车信息
    cart_list = Cart.objects_logic.get_cart_list_by_id_list(card_id_list=cart_id_list)
    cart_id_list = ','.join(cart_id_list)  # '1,2,3'
    return render(request, 'place_order.html', {'addr': addr, 'carr_list': cart_list, 'cart_id_list': cart_id_list})


@require_POST
@login_required
@transaction.atomic
def order_commit(request):
    '''
    提交订单
    '''
    # 接收订单信息
    addr_id = request.POST.get('addr_id')
    pay_method = request.POST.get('pay_method')
    cart_id_list = request.POST.get('cart_id_list')

    # 获取passport_id
    passport_id = request.session.get('passport_id')

    # 组织订单id　20170903160533+passport_id
    order_id = datetime.now().strftime('%Y%m%d%H%M%S')+str(passport_id)
    transit_price = 10.0

    # 统计用户购买的商品总数和总价格
    cart_id_list = cart_id_list.split(',')
    total_count, total_price = Cart.objects.get_goods_count_and_amout_by_id_list(cart_id_list=cart_id_list)
    # 设置一个保存点
    save_id = transaction.savepoint()
    try:
        # 生成一个订单基本信息
        OrderBasic.objects.add_one_order_basic_info(order_id=order_id,passport_id=passport_id,addr_id=addr_id,
                                                    total_count=total_count, total_price=total_price,transit_price=transit_price,
                                                    pay_method=pay_method)

        # 遍历生成订单详情信息记录
        cart_list = Cart.objects.get_cart_list_by_id_list(card_id_list=cart_id_list)
        for cart_info in cart_list:
            # 判断商品的库存是否充足
            if cart_info.goods_count < cart_info.goods.goods_stock:
                # 组织订单详情信息
                goods_id = cart_info.goods.id
                goods_count = cart_info.goods_count
                goods_price = cart_info.goods.goods_price
                OrderDetail.objects.add_one_detail_info(order_id=order_id,goods_id=goods_id,goods_count=goods_count,
                                                        goods_price=goods_price)
                # 减少商品的库存，增加销售量
                cart_info.goods.goods_stock = cart_info.goods.goods_stock - cart_info.goods_count
                cart_info.goods.goods_sales = cart_info.goods.goods_sales + cart_info.goods_count
                cart_info.save()

                # 删除购物车记录信息
                cart_info.delete()

            else:
                # 库存不足
                # 如果发生异常进行回滚
                transaction.savepoint_rollback(save_id)
                return JsonResponse({'res': 0, 'content':'库存不足'})
    except Exception as e:
        # 如果发生异常进行回滚
        transaction.savepoint_rollback(save_id)
        return JsonResponse({'res': 0, 'content':'服务器错误'})

    # 提交事务
    transaction.savepoint_commit(save_id)
    return JsonResponse({'res': 1})














