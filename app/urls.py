# coding:utf-8
from django.conf.urls import url
import app.views

urlpatterns = [
    url(r'^$', app.views.index),
    url(r'^product$', app.views.product),
    url(r'^product_classify$', app.views.product_classify_operate),
    url(r'^classify/operate$', app.views.product_classify_operate),
    url(r'^supplier$', app.views.supplier),
    url(r'^order$', app.views.order),
    url(r'^orderitems$', app.views.orderitem_list),
    url(r'^warehousing$', app.views.warehousing),
    url(r'^reserve$', app.views.reserve),
]
