from django.db import models
from db.base_model import BaseModel
from db.base_manage import BaseModelManager
from django.db.models import Sum  # 导入聚合类
from df_goods.models import Image

# Create your models here.

class CartLogicManger(BaseModelManager):
    '''
    购物车逻辑模型管理器类
    '''
    def get_cart_list_by_passport(self, passport_id):
        '''
        根据passport_id获取购物车信息
        '''
        cart_list = Cart.objects.get_cart_list_by_passport(passport_id=passport_id)
        for cart_info in cart_list:
            # 获取商品的图片
            img = Image.objects.get_image_by_goods_id(goods_id=cart_info.goods.id)
            cart_info.goods.img_url = img.img_url
        return cart_list

    def get_cart_list_by_id_list(self, card_id_list):
        '''
        根据cart_id_list查询购物车信息
        '''
        cart_list = Cart.objects.get_object_list(filters={'id__in': card_id_list})
        for cart_info in cart_list:
            # 获取商品的图片
            img = Image.objects.get_image_by_goods_id(goods_id=cart_info.goods.id)
            cart_info.goods.img_url = img.img_url
        return cart_list


class CartManager(BaseModelManager):
    '''
    购物车模型管理器类
    '''
    def get_one_cart_info_by_id(self, cart_id):
        '''
        根据id查询购物车记录
        '''
        cart_info = self.get_one_object(id=cart_id)
        return cart_info

    def get_one_cart_info(self, passport_id, goods_id):
        '''
        判断用户的购物车中是否添加过该商品
        '''
        cart_info = self.get_one_object(passport_id=passport_id, goods_id=goods_id)
        return cart_info

    def add_one_cart_info(self, passport_id, goods_id, goods_count):
        '''
        添加购物车信息
        '''
        # 1.判断用户的购物车中是否已经添加过该商品
        cart_info = self.get_one_cart_info(passport_id=passport_id, goods_id=goods_id)
        if cart_info is None:
            # 用户购物车中没有添加过该商品
            cart_info = self.create_one_object(passport_id=passport_id, goods_id=goods_id, goods_count=goods_count)
        else:
            # 用户购物车中添加过该商品
            cart_info.goods_count = cart_info.goods_count + goods_count
            cart_info.save()
        return cart_info

    def get_cart_count_by_passport(self, passport_id):
        '''
        根据passport_id获取用户购物车中商品的数目
        '''
        res_dict = self.get_object_list(filters={'passport_id': passport_id}).aggregate(Sum('goods_count'))
        # print(res_dict) {'goods_count__sum': 16}
        res = res_dict['goods_count__sum']
        if res is None:
            res = 0
        return res

    def get_cart_list_by_passport(self, passport_id):
        '''
        根据passport_id获取购物车信息
        '''
        cart_list = self.get_object_list(filters={'passport_id': passport_id})
        return cart_list

    def update_cart_info_by_passport(self, passport_id, goods_id, goods_count):
        '''
        更新用户购物车中商品的数目
        '''
        cart_info = self.get_one_cart_info(passport_id=passport_id, goods_id=goods_id)
        if cart_info:
            # 购物车中有信息
            # 判断更新的数量是否大于商品的库存
            if cart_info.goods.goods_stock < goods_count:
                # 更新失败
                return False
            else:
                # 进行更新
                cart_info.goods_count = goods_count
                cart_info.save()
                return True
        else:
            # 如果获取不到，可以新增一条
            self.add_one_cart_info(passport_id=passport_id, goods_id=goods_id, goods_count=goods_count)
            return True

    def get_cart_list_by_id_list(self, card_id_list):
        '''
        根据cart_id_list查询购物车信息
        '''
        cart_list = self.get_object_list(filters={'id__in': card_id_list})
        return cart_list

    def get_goods_count_and_amout_by_id_list(self, cart_id_list):
        '''
        统计用户购买的商品的总数和总价格
        '''
        total_count,total_price = 0,0
        cart_list = self.get_object_list(filters={'id__in': cart_id_list})
        for cart_info in cart_list:
            total_count += cart_info.goods_count
            total_price += cart_info.goods_count*cart_info.goods.goods_price
        return total_count,total_price


class Cart(BaseModel):
    '''
    购物车模型类
    '''
    passport = models.ForeignKey('db_user.Passport', verbose_name='账户')
    goods = models.ForeignKey('df_goods.Goods', verbose_name='商品')
    goods_count = models.IntegerField(default=1, verbose_name='商品数目')

    objects = CartManager()
    objects_logic = CartLogicManger()

    class Meta:
        db_table = 's_cart'

