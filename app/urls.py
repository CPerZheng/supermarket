# encoding=utf-8
from django.conf.urls import url
import app.views

urlpatterns = [
    url(r'^$', app.views.index),
    url(r'product', app.views.product),
]
