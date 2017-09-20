# 定义一个模型管理器基类
from django.db import models
import copy


class BaseModelManager(models.Manager):
    '''
    模型管理器抽象基类
    '''
    def get_all_valid_fields(self):
        '''
        返回self模型管理器对象所在模型类的属性的列表
        '''
        # 1.获取self所在的模型类
        model_class = self.model
        # 2.获取model_class模型类的属性的列表
        attr_list = model_class._meta.get_fields()
        str_attr_list = []
        for attr in attr_list:
            if isinstance(attr, models.ForeignKey):
                str_attr = '%s_id'%attr.name
            else:
                str_attr = attr.name
            str_attr_list.append(str_attr)
        # 3.获取model_class模型类的属性的字符串列表
        return str_attr_list

    def create_one_object(self, **kwargs):
        '''
        创建一个self模型管理器对象所在的模型类的对象
        '''
        # 1.获取self.model模型类的属性的字符串列表
        valid_fields = self.get_all_valid_fields()
        # 2.拷贝kwargs参数
        kws = copy.copy(kwargs)
        # 3.去除self.model模型类的无效属性
        # for key in kws.keys():
        for key in kws:
            if key not in valid_fields:
                # 不是模型类的有效属性
                kwargs.pop(key)

        # print(kwargs)
        # 4.获取self所在的模型类
        model_class = self.model
        obj = model_class(**kwargs)
        obj.save()
        # 5.返回这个对象
        return obj

    def get_one_object(self, **filters):
        '''
        根据条件查询self.model类的对象
        '''
        try:
            obj = self.get(**filters)
            print('222', obj)
        except self.model.DoesNotExist:
            obj = None
            print(333)
        return obj

    def get_object_list(self, filters={}, exclude_filters={}, order_by=('-pk',)):
        '''
        根据条件获取self.model对应的查询集
        '''
        # 解包传入的参数
        object_list = self.filter(**filters).exclude(**exclude_filters).order_by(*order_by)
        return object_list










