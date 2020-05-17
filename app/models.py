# encoding=utf-8
from django.contrib.auth.models import User
from django.db import models
from supermarket.settings import PERMS

# Create your models here.
# 商品保存条件
pre_type = [(u'01', u'干燥保存'), (u'02', u'低温保存')]

# 商品状态
pro_state = [(u'01', u'未入库'), (u'02', u'已入库'), (u'03', u'已出库'), (u'04', u'退货')]


class Classify(models.Model):
    """商品类型"""
    name = models.CharField(max_length=30, verbose_name="商品类型名称")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class Supplier(models.Model):
    """供应商"""
    supplier_name = models.CharField(max_length=50, verbose_name="供应商名称")
    name = models.CharField(max_length=30, blank=True, verbose_name="联系人姓名")
    phone = models.CharField(max_length=30, blank=True, verbose_name="联系人电话")
    card_num = models.CharField(max_length=30, blank=True, verbose_name="银行卡号")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class Employee(models.Model):
    """员工信息"""
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=30, verbose_name="员工姓名")
    phone = models.CharField(max_length=20, blank=True, verbose_name="联系电话")
    position = models.CharField(max_length=30, blank=True, verbose_name="职位")

    class Meta:
        permissions = PERMS

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class Product(models.Model):
    """商品信息"""
    name = models.CharField(max_length=30, verbose_name="商品名称")
    pro_num = models.CharField(max_length=30, null=True, verbose_name="商品编号")
    classify = models.ForeignKey(Classify, related_name="classify_product", null=True, on_delete=models.SET_NULL,
                                 verbose_name="商品类型")
    date_of_manufacture = models.DateTimeField(null=True, blank=True, verbose_name="生产日期")  # format=%Y-%m-%d %H:%M:%S
    guarantee_period = models.DateTimeField(null=True, blank=True, verbose_name="保质期")  # format=%Y-%m-%d %H:%M:%S
    preserve = models.CharField(max_length=30, choices=pre_type, verbose_name="存储条件")
    unit_of_measurement = models.CharField(max_length=30, null=True, blank=True, verbose_name="计量单位")
    supplier = models.ForeignKey(Supplier, related_name="supplier_product", null=True, on_delete=models.SET_NULL,
                                 verbose_name="供应商")
    last_update = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class Order(models.Model):
    """订单表"""
    order_num = models.CharField(max_length=30, verbose_name="订单编号")
    cost = models.FloatField(null=True, verbose_name="订单总额")
    order_state = models.CharField(max_length=30, choices=pro_state, verbose_name="订单状态")
    operator = models.ForeignKey(User, related_name="operator", blank=True, null=True, on_delete=models.SET_NULL,
                                 verbose_name="操作人员")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.order_num

    class Meta:
        ordering = ['id']


class OrderItem(models.Model):
    """订单详情表"""
    product_name = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL, verbose_name="商品名称")
    order_number = models.ForeignKey(Order, related_name="order_number", blank=True, null=True,
                                     on_delete=models.SET_NULL, verbose_name="订单编号")
    num = models.IntegerField(null=True, verbose_name="商品数量")
    unit_price = models.FloatField(null=True, verbose_name="商品单价")
    total_price = models.FloatField(null=True, verbose_name="商品总价")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.order_number.order_num

    class Meta:
        ordering = ['id']


class Warehousing(models.Model):
    """入库信息表"""
    ware_num = models.CharField(max_length=30, verbose_name="入库编号")
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL, verbose_name="入库商品")
    # num = models.IntegerField(null=True, verbose_name="入库数量")
    create_time = models.DateTimeField(auto_now_add=True)
    last_time = models.DateTimeField(null=True, blank=True)
    remark = models.CharField(max_length=255, null=True, blank=True, verbose_name="备注")

    def __str__(self):
        return self.ware_num

    class Meta:
        ordering = ['id']


class Reserve(models.Model):
    """库存表"""
    reserve_id = models.CharField(max_length=30, verbose_name="库存编号")
    warenum = models.ForeignKey(Warehousing, null=True, on_delete=models.SET_NULL, verbose_name="入库编号")
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL, verbose_name="库存商品")
    reserve_num = models.IntegerField(null=True, verbose_name="库存数量")
    last_time = models.DateTimeField(null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reserve_id

    class Meta:
        ordering = ['id']


class ExWareHousing(models.Model):
    """出库信息表"""
    ex_ware_num = models.CharField(max_length=30, verbose_name="出库编号")
    ex_product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL, verbose_name="出库商品")
    ex_reserve = models.ForeignKey(Reserve, null=True, on_delete=models.SET_NULL, verbose_name="库存编号")
    out_num = models.IntegerField(null=True, verbose_name="出库数量")
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ex_ware_num

    class Meta:
        ordering = ['id']
