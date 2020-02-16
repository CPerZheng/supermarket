# coding:utf-8
import datetime
import random

from django.http import JsonResponse


def write_json(obj):
    return JsonResponse(obj)


# 商品编号
def product_num_id():
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    cl = []
    c = 0
    while c < 2:
        ch = random.choice(alphabet)
        cl.append(ch)
        c += 1
    characters = ''.join(cl)
    num = str(random.randint(1000, 5000))

    return '{0}{1}'.format(str(characters), num)


# 订单编号
def order_num_id():
    now = datetime.datetime.now()
    oni = now.strftime('%Y%m%d%H%M%S')
    return str(oni)

