# coding:utf-8
from django.conf.urls import url
import app.views

urlpatterns = [
    url(r'^$', app.views.index),
    url(r'^login$', app.views.login),
    url(r'^logout$', app.views.logout),
    url(r'^product$', app.views.product),
    url(r'^product_classify$', app.views.product_classify_operate),
    url(r'^classify/operate$', app.views.product_classify_operate),
    url(r'^supplier$', app.views.supplier),
    url(r'^order$', app.views.order),
    url(r'^orderitems$', app.views.orderitem_list),
    url(r'^warehousing$', app.views.warehousing),
    url(r'^reserve$', app.views.reserve),
    url(r'^ex_ware_housing$', app.views.exwarehousing),
    url(r'^ex_ware_operate$', app.views.exwareoperate),
    url(r'^employee/list$', app.views.employee_list),
    url(r'^employee/operate$', app.views.employee_operate),
    url(r'^employee/detail$', app.views.employee_detail),
    url(r'^operate/tips$', app.views.operate_tip),
]
