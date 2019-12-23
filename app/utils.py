# encoding=utf-8
from django.http import JsonResponse


def write_json(obj):
    return JsonResponse(obj)

