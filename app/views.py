# encoding=utf-8
from django.core.paginator import Paginator
from django.shortcuts import render
from app.models import Classify
from app.utils import write_json


# Create your views here.
def index(request):
    return render(request, 'app/index.html')


def product(request):
    if request.method == 'GET':
        
        return render(request, "app/product.html")


def product_classify_operate(request):
    """classify operate function"""
    if request.method == 'GET':
        search_word = request.GET.get('classify_search', '').strip()  # 获取查询关键字
        pc_list = Classify.objects.all()
        if search_word:
            pc_list = Classify.objects.filter(name__contains=search_word)

        p = int(request.GET.get('p', 1))
        limit = int(request.GET.get('limit', 10))
        paginator = Paginator(pc_list, limit)
        page = paginator.page(p)
        data = {
            'classify_search': search_word,
            'pc_list': page.object_list,
            'paginator': page,
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
