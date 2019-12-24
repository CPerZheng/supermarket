# encoding=utf-8
from django.conf.urls import url
import app.views

urlpatterns = [
    url(r'^$', app.views.index),
    url(r'^product$', app.views.product),
    url(r'^product_classify$', app.views.product_classify_operate),
    url(r'^classify/operate$', app.views.product_classify_operate),
    url(r'^supplier$', app.views.supplier),
]
