from django.db import models
from tinymce.models import HTMLField
from db.base_model import BaseModel
from db.base_manage import BaseModelManager
from df_goods.enums import *

# Create your models here.


class GoodsInfo(models.Model):
    '''
    商品信息模型类
    '''
    goods_info = HTMLField(verbose_name='商品描述')


class GoodsLogicManger(BaseModelManager):
    '''
    商品逻辑模型管理器
    '''
    def get_goods_list_by_type(self, goods_type_id, limit=None, sort='default'):
        '''
        根据商品类型id获取商品信息
        '''
        goods_list = Goods.objects.get_goods_list_by_type(goods_type_id=goods_type_id, limit=limit, sort=sort)
        # 遍历获取每一个商品信息
        for goods in goods_list:
            # 根据商品的id获取商品的图片
            img = Image.objects.get_image_by_goods_id(goods_id=goods.id)  # QuerySet Image
            # 给goods对象添加一个属性img_url，用户记录商品图片路径
            goods.img_url = img.img_url
        return goods_list

    def get_goods_by_id(self, goods_id):
        '''
        根据商品id查询商品信息
        '''
        goods = Goods.objects.get_goods_by_id(goods_id=goods_id)
        # 获取商品goods的图片
        img = Image.objects.get_image_by_goods_id(goods_id=goods_id)
        # 给goods对象增加一个属性img_url，用户记录商品图片路径
        goods.img_url = img.img_url
        return goods


class GoodsManger(BaseModelManager):
    '''
    商品模型管理器类
    '''
    def get_goods_by_id(self, goods_id):
        '''
        根据商品id查询商品信息
        '''
        goods = self.get_one_object(id=goods_id)
        return goods

    def get_goods_list_by_type(self, goods_type_id, limit=None, sort='default'):
        '''
        根据商品类型id获取商品信息
        '''
        if sort == 'new':
            # 查询新品信息
            order_by = ('-create_time',)
        elif sort == 'price':
            # 按价格查询商品信息
            order_by = ('goods_price',)
        elif sort == 'hot':
            # 按热度查询商品信息
            order_by = ('-goods_sales',)
        else:
            order_by = ('-pk',)
        goods_list = self.get_object_list(filters={'goods_type_id': goods_type_id}, order_by=order_by)
        # 对结果集进行限制
        if limit:
            goods_list = goods_list[:limit]
        return goods_list


class Goods(BaseModel):
    '''
    商品模型类
    '''
    goods_type_choice = (
        (FRUIT, GOODS_TYPE[FRUIT]),
        (SEAFOOD, GOODS_TYPE[SEAFOOD]),
        (MEAT, GOODS_TYPE[MEAT]),
        (EGGS, GOODS_TYPE[EGGS]),
        (VEGETABLES, GOODS_TYPE[VEGETABLES]),
        (FROZEN, GOODS_TYPE[FROZEN])
    )

    # 1.海鲜水果　2.海鲜水产　3.猪牛羊肉　4.禽类蛋品　5.新鲜蔬菜　6.速冻食品
    goods_type_id = models.SmallIntegerField(choices=goods_type_choice, default=FRUIT, verbose_name='商品类型')
    goods_name = models.CharField(max_length=20, verbose_name='商品名称')
    goods_sub_title = models.CharField(max_length=256, verbose_name='商品副标题')
    goods_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')
    transit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品运费')
    goods_unite = models.CharField(max_length=20, verbose_name='商品单位')
    goods_info = HTMLField(verbose_name='商品描述')
    goods_stock = models.IntegerField(default=0, verbose_name='商品库存')
    goods_sales = models.IntegerField(default=0, verbose_name='商品销量')
    # 1.上线商品　0.下线商品
    goods_status = models.SmallIntegerField(default=1, verbose_name='商品状态')

    objects = GoodsManger()
    objects_logic = GoodsLogicManger()

    class Meta:
        db_table = 's_goods'


class ImageManger(BaseModelManager):
    '''
    商品图片模型管理器
    '''
    def get_image_by_goods_id(self, goods_id):
        '''
        根据商品的id获取商品的图片路径
        '''
        # 获取商品图片的查询集
        images = self.get_object_list(filters={'goods_id': goods_id})
        if images.exists():
            # 商品有对应的图片
            images = images[0]
        else:
            # 商品没有图片，给images增加一个img_url属性
            images.img_url = ''
        return images

    def get_images_by_goods_id_list(self, goods_id_list):
        '''
        根据商品id列表获取商品图片信息
        '''
        images = self.get_object_list(filters={'goods_id__in': goods_id_list})
        return images


class Image(BaseModel):
    '''
    商品图片模型类
    '''
    goods = models.ForeignKey('Goods', verbose_name='所属商品')
    img_url = models.ImageField(upload_to='goods/', verbose_name='图片路径')
    is_def = models.BooleanField(default=False, verbose_name='是否默认')

    objects = ImageManger()

    class Meta:
        db_table = 's_goods_image'


class BrowserHistoryLogicManager(BaseModelManager):
    '''
    用户浏览历史记录模型逻辑管理器类
    '''
    def get_browse_list_by_passport(self, passport_id):
        '''
        根据passport_id获取对应用户的浏览记录
        '''
        browsed_li = self.get_object_list(filters={'passport_id': passport_id}, order_by=('-update_time',))
        for browsed in browsed_li:
            image = Image.objects.get_image_by_goods_id(goods_id=browsed.goods.id)
            browsed.goods.img_url = image.img_url
        return browsed_li


class BrowserHistoryManager(BaseModelManager):
    '''
    用户浏览历史记录管理模型类
    '''
    def get_one_history(self, passport_id, goods_id):
        '''
        查询用户是否浏览过某个商品
        '''
        browsed = self.get_one_object(passport_id=passport_id, goods_id=goods_id)
        return browsed

    def add_one_history(self, passport_id, goods_id):
        '''
        添加用户的一条浏览记录
        '''
        # 1.去去查找用户是否浏览过该商品
        browsed = self.get_one_history(passport_id=passport_id, goods_id=goods_id)
        # 2.如果用户浏览过该商品，则更新update_time,否则插入一条新的浏览记录
        if browsed:
            # 调用browsed.save方法会自动更新update_time
            browsed.save()
        else:
            browsed = self.create_one_object(passport_id=passport_id, goods_id=goods_id)
        return browsed

    def get_browse_list_by_passport(self, passport_id):
        '''
        根据passport_id获取对应用户的浏览记录
        '''
        browsed_li = self.get_object_list(filters={'passport_id': passport_id}, order_by=('-update_time',))
        return browsed_li


class BrowserHistory(BaseModel):
    '''
    用户浏览历史记录类
    '''
    passport = models.ForeignKey('db_user.Passport', verbose_name='账户')
    goods = models.ForeignKey('Goods', verbose_name='商品')

    objects = BrowserHistoryManager()
    objects_logic = BrowserHistoryLogicManager()

    class Meta:
        db_table = 's_browse_history'





















