# encoding=utf-8
from django.contrib.auth.models import User
from django.db import models
from supermarket.settings import PERMS

# Create your models here.
# 商品保存条件
pre_type = [(u'01', u'干燥保存'), (u'02', u'低温保存')]


# 商品状态
pro_state = [(u'01', u'正常'), (u'02', u'退货')]


class Classify(models.Model):
    """商品类型"""
    name = models.CharField(max_length=30, help_text="商品类型名称")
    create_time = models.DateTimeField(auto_now_add=True, help_text="创建时间")

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['id']


class Supplier(models.Model):
    """供应商"""
    supplier_name = models.CharField(max_length=50, help_text="供应商名称")
    name = models.CharField(max_length=30, blank=True, help_text="联系人姓名")
    phone = models.CharField(max_length=30, blank=True, help_text="联系人电话")
    card_num = models.CharField(max_length=30, blank=True, help_text="银行卡号")
    create_time = models.DateTimeField(auto_now_add=True, help_text="创建时间")

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['id']


class Employee(models.Model):
    """员工信息"""
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=30, help_text="员工姓名")
    phone = models.CharField(max_length=20, blank=True, help_text="联系电话")
    position = models.CharField(max_length=30, blank=True, help_text="职位")

    class Meta:
        permissions = PERMS

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['id']


class Product(models.Model):
    """商品信息"""
    name = models.CharField(max_length=30, help_text="商品名称")
    classify = models.ForeignKey(Classify, null=True, on_delete=models.SET_NULL, help_text="商品类型")
    palce_of_origin = models.FloatField(null=True, help_text="产地")
    date_of_manufacture = models.DateTimeField(null=True, help_text="生产日期")  # format=%Y-%m-%d %H:%M:%S
    preserve = models.CharField(max_length=30, choices=pre_type, help_text="存储条件")
    supplier = models.ForeignKey(Supplier, null=True, on_delete=models.SET_NULL, help_text="供应商")

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['id']


class Order(models.Model):
    """进货订单表"""
    order_num = models.CharField(max_length=30, help_text="订单编号")
    cost = models.FloatField(null=True, help_text="订单总额")
    order_state = models.CharField(max_length=30, choices=pro_state, help_text="订单状态")
    operator = models.ForeignKey(User, related_name="operator", null=True, on_delete=models.SET_NULL, help_text="操作人员")
    create_time = models.DateTimeField(auto_now_add=True, help_text="创建时间")

    def __unicode__(self):
        return self.order_num

    class Meta:
        ordering = ['id']


class OrderItem(models.Model):
    """订单详情表"""
    product_name = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL, help_text="商品名称")
    num = models.IntegerField(null=True, help_text="商品数量")
    nuit_price = models.FloatField(null=True, help_text="商品单价")
    total_price = models.FloatField(null=True, help_text="商品总价")
    create_time = models.DateTimeField(auto_now_add=True, help_text="创建时间")

    def __init__(self):
        return self.id

    class Meta:
        ordering = ['id']


class Warehousing(models.Model):
    """入库信息表"""
    ware_num = models.CharField(max_length=30, help_text="入库编号")
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL, help_text="入库商品")
    num = models.IntegerField(null=True, help_text="入库数量")
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.ware_num

    class Meta:
        ordering = ['id']


class ExWareHousing(models.Model):
    """出库信息表"""
    ex_ware_num = models.CharField(max_length=30, help_text="出库编号")
    ex_product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL, help_text="出库商品")
    out_num = models.IntegerField(null=True, help_text="出库数量")
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.ex_ware_num

    class Meta:
        ordering = ['id']

