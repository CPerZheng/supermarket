# encoding=utf-8
from django.core.paginator import Paginator
from django.shortcuts import render
from app.models import Classify, Supplier
from app.utils import write_json


# Create your views here.
def index(request):
    return render(request, 'app/index.html')


def product_classify_operate(request):
    """classify operate function"""
    if request.method == 'GET':
        search_word = request.GET.get('classify_search', '').strip()  # 获取查询关键字
        pc_list = Classify.objects.all()
        if search_word:
            pc_list = Classify.objects.filter(name__contains=search_word)

        total_count = pc_list.count()
        p = int(request.GET.get('page', 1))  # 当前页
        # limit = int(request.GET.get('limit', 10))  # 每页限定数据数量
        paginator = Paginator(pc_list, 2)  # 分页器
        page = paginator.page(p)  # 当前页数据
        data = {
            'classify_search': search_word,
            'pc_list': page.object_list,
            'paginator': page,
            'total_count': total_count,
        }
        return render(request, "app/product_classify.html", data)
    if request.method == 'POST':
        data = request.POST.dict()
        pc_action = data.get('action')
        pro_classify = data.get('classify_name')
        if pc_action == "add":
            has_classify = Classify.objects.filter(name=pro_classify)
            if has_classify:
                return write_json({"errno": "1", "msg": "this classify had already add!"})
            else:
                Classify.objects.create(name=pro_classify)
                return write_json({"errno": "0", "msg": "success"})
        elif pc_action == "edit":
            classify_id = data.get('classify_id')
            Classify.objects.filter(id=classify_id).update(name=pro_classify)
            return write_json({"errno": "0", "msg": "success"})
        elif pc_action == "del":
            classify_id = data.get('classify_id')
            if classify_id:
                Classify.objects.filter(id=classify_id).delete()
                return write_json({"errno": "0", "msg": "success"})
            else:
                return write_json({"errno": "1", "msg": "lost the id!"})
    else:
        return write_json({"errno": "2", "msg": "not action to do!"})


def supplier(request):
    """supplier operate function"""
    if request.method == 'GET':
        search_word = request.GET.get('supplier_search', '').strip()  # 获取查询关键字
        ps_list = Supplier.objects.all()
        if search_word:
            ps_list = Supplier.objects.filter(name__contains=search_word)

        total_count = ps_list.count()
        p = int(request.GET.get('page', 1))  # 当前页
        # limit = int(request.GET.get('limit', 10))  # 每页限定数据数量
        paginator = Paginator(ps_list, 2)  # 分页器
        page = paginator.page(p)  # 当前页数据
        data = {
            'supplier_search': search_word,
            'ps_list': page.object_list,
            'paginator': page,
            'total_count': total_count,
        }
        return render(request, "app/supplier.html", data)
    if request.method == 'POST':
        data = request.POST.dict()
        ps_action = data.get('action')
        pro_supplier = data.get('supplier_name')

        if ps_action == "add":
            has_supplier = Supplier.objects.filter(name=pro_supplier)
            if has_supplier:
                return write_json({"errno": "1", "msg": "this classify had already add!"})
            else:
                add_data = {
                    'supplier_name': data.get('pro_supplier'),
                    'name': data.get('supplier_name'),
                    'phone': data.get('supplier_phone'),
                    'card_num': data.get('supplier_card_num')
                }
                Supplier.objects.create(**add_data)
                return write_json({"errno": "0", "msg": "success"})

        elif ps_action == "edit":
            supplier_id = data.get('supplier_id')
            edit_data = {
                'supplier_name': data.get('supplier_name'),
                'name': data.get('edit_name'),
                'phone': data.get('supplier_phone'),
                'card_num': data.get('supplier_card_num')
            }
            if supplier_id:
                Supplier.objects.filter(id=supplier_id).update(**edit_data)
                return write_json({"errno": "0", "msg": "success"})
            else:
                return write_json({"errno": "1", "msg": "lost the id!"})

        elif ps_action == "del":
            supplier_id = data.get('supplier_id')
            if supplier_id:
                Supplier.objects.filter(id=supplier_id).delete()
                return write_json({"errno": "0", "msg": "success"})
            else:
                return write_json({"errno": "1", "msg": "lost the id!"})
    else:
        return write_json({"errno": "2", "msg": "not action to do!"})


def product(request):
    if request.method == 'GET':
        return render(request, "app/product.html")

