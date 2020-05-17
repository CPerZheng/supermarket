# coding:utf-8
import datetime
import random

from django.http import JsonResponse


def write_json(obj):
    return JsonResponse(obj)


# 商品/库存编号
def product_num_id(n):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    cl = []
    c = 0
    al_num = 0
    # 判断是商品编号还是库存编号创建操作
    # 商品编号创建:n=1
    # 库存编号创建:n=2
    # 出库编号创建:n=3
    if n == 1:
        al_num = 2
        num = str(random.randint(1000, 5000))
    elif n == 2:
        al_num = 4
        num = str(random.randint(5001, 9000))
    elif n == 3:
        al_num = 3
        num = str(random.randint(9001, 15000))

    while c < al_num:
        ch = random.choice(alphabet)
        cl.append(ch)
        c += 1
    characters = ''.join(cl)

    return '{0}{1}'.format(str(characters), num)


# 订单编号
def order_num_id():
    now = datetime.datetime.now()
    oni = now.strftime('%Y%m%d%H%M%S')
    return str(oni)
