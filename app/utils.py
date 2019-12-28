# coding:utf-8
import random

from django.http import JsonResponse


def write_json(obj):
    return JsonResponse(obj)


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

