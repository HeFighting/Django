from django.db import models
from db.base_model import BaseModel  # 导入模型抽象基类
from utils.get_hash import get_hash  #　导入加密函数
from db.base_manage import BaseModelManager

# Create your models here.


class PassportManager(BaseModelManager):
    '''
    用户账户类模型管理器
    '''
    # def add_one_passport(self, username, password, email):
    #     '''
    #     添加一个用户注册信息
    #     '''
    #     # 1.获取模型管理器所在的模型类
    #     model_class = self.model
    #     # 2.创建模型类对象
    #     p = model_class()
    #
    #     p.username = username
    #     p.password = get_hash(password)
    #     p.email = email
    #     p.save()
    #     # 3.将创建好的对象返回, 这句不加也不会有影响
    #     return p

    def add_one_passport(self, username, password, email):
        '''
        添加一个用户注册信息
        '''
        passport = self.create_one_object(username = username, password=get_hash(password), email = email)
        return passport

    # def get_one_passport(self, username, password=None):
    #     '''
    #     获取一个查询对象
    #     '''
    #     try:
    #         if password is None:
    #             # 根据用户名来查询账户信息
    #             p = self.get(username=username)
    #         else:
    #             # 根据用户名和密码来查询账户信息
    #             p = self.get(username=username, password=get_hash(password))
    #             # p = self.filter(username=username).filter(password=get_hash(password))
    #     except self.model.DoesNotExist:
    #         p = None
    #     return p

    def get_one_passport(self, username, password=None):
        '''
        获取一个查询对象
        '''
        if password is None:
            # 根据用户名查询账户信息
            passport = self.get_one_object(username=username)
        else:
            # 根据用户名和密码查询账户信息
            passport = self.get_one_object(username=username, password=password)
            print(passport,'111')
        return passport


class Passport(BaseModel):
    '''
    用户账户类
    '''
    username = models.CharField(max_length=20, verbose_name='用户名')
    password = models.CharField(max_length=40, verbose_name='密码')
    email = models.EmailField(verbose_name='邮箱')  # 可以验证是否是一个有效的邮箱信息

    objects = PassportManager()

    # def __init__(self, username, password, email):
    #     self.username = username
    #     self.password = password
    #     self.email = email
    # model.Model中自带函数，直接传参数就可以
    class Meta:
        db_table = 's_user_account'  # 指定表名


class AddressManager(BaseModelManager):
    '''
    地址模型管理器类
    '''
    def get_default_address(self, passport_id):
        '''
        获取账户的默认收货地址
        '''
        # 根据passport_id获取账户的默认收货地址
        def_addr = self.get_one_object(passport_id=passport_id, is_def=True)
        return def_addr

    def add_one_address(self, passport_id, recipient_name, recipient_addr, zip_code, recipient_phone):
        '''
        添加一个收货地址
        '''
        def_addr = self.get_default_address(passport_id)
        if def_addr is None:
            # 用户不存在默认收货地址
            addr = self.create_one_object(passport_id=passport_id, recipient_name=recipient_name,
                                          recipient_addr=recipient_addr,zip_code=zip_code,
                                          recipient_phone=recipient_phone,is_def=True)
        else:
            # 用户已有默认收货地址
            addr = self.create_one_object(passport_id=passport_id, recipient_name=recipient_name,
                                          recipient_addr=recipient_addr,zip_code=zip_code,
                                          recipient_phone=recipient_phone)
        return addr


class Address(BaseModel):
    '''
    用户地址类
    '''
    passport = models.ForeignKey('Passport', verbose_name='所属账户')
    recipient_name = models.CharField(max_length=20, verbose_name='收件人')
    recipient_addr = models.CharField(max_length=256, verbose_name='收件地址')
    recipient_phone = models.CharField(max_length=11, verbose_name='联系电话')
    zip_code = models.CharField(max_length=6, verbose_name='邮编')
    is_def = models.BooleanField(default=False, verbose_name='是否默认')

    objects = AddressManager()

    class Meta:
        db_table = 's_user_address'


