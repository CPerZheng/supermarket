# coding:utf-8
import datetime
import json

from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from app.models import Classify, Supplier, Product, Order, OrderItem, Reserve, Warehousing, ExWareHousing, Employee
from app.utils import write_json, product_num_id, order_num_id
from supermarket.settings import PERMS

# Create your views here.
# edit by cperzheng@163.com


@user_passes_test(lambda u: u.is_staff, login_url='/login')
def index(request):
    return render(request, 'app/index.html')


def login(request):
    """login function"""
    if request.method == 'POST':
        name = request.POST.get('username', '')
        psd = request.POST.get('password', '')
        user = auth.authenticate(username=name, password=psd)
        print(user)
        if user is not None:
            if user.is_active and user.is_staff:
                auth.login(request, user)
                return HttpResponseRedirect('/')
            else:
                return redirect('/operate/tips?msg='+u'账号出现异常, 请联系超级管理员')
        else:
            return redirect('operate/tips?msg='+u'账号密码错误')

    if request.user.is_authenticated:
        if request.user.is_staff:
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/logout')
    return render(request, 'app/login.html')


def logout(request):
    """logout function"""
    auth.logout(request)
    return HttpResponseRedirect('/login')


@user_passes_test(lambda u: u.is_staff, login_url='/login')
@permission_required('app.product_manage')
def product_classify_operate(request):
    """classify operate function"""
    if request.method == 'GET':
        search_word = request.GET.get('classify_search', '').strip()  # 获取查询关键字
        pc_list = Classify.objects.all()
        if search_word:
            pc_list = Classify.objects.filter(name__contains=search_word)

        total_count = pc_list.count()
        # print(total_count)
        p = int(request.GET.get('page', 1))  # 当前页
        limit = int(request.GET.get('limit', 10))  # 每页限定数据数量
        paginator = Paginator(pc_list, limit)  # 分页器
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


@user_passes_test(lambda u: u.is_staff, login_url='/login')
@permission_required('app.product_manage')
def supplier(request):
    """supplier operate function"""
    if request.method == 'GET':
        search_word = request.GET.get('supplier_search', '').strip()  # 获取查询关键字
        ps_list = Supplier.objects.all()
        if search_word:
            ps_list = Supplier.objects.filter(name__contains=search_word)

        total_count = ps_list.count()
        p = int(request.GET.get('page', 1))  # 当前页
        limit = int(request.GET.get('limit', 10))  # 每页限定数据数量
        paginator = Paginator(ps_list, limit)  # 分页器
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


@user_passes_test(lambda u: u.is_staff, login_url='/login')
@permission_required('app.product_manage')
def product(request):
    """product operate function"""
    if request.method == 'GET':
        p_classify = Classify.objects.all()
        p_supplier = Supplier.objects.all()

        search_word = request.GET.get('product_search', '').strip()  # 获取查询关键字
        pr_list = Product.objects.all()
        if search_word:
            find_product = (
                    Q(name__icontains=search_word) |
                    Q(pro_num__icontains=search_word) |
                    Q(classify__name__contains=search_word)
            )
            pr_list = Product.objects.filter(find_product)

        total_count = pr_list.count()
        p = int(request.GET.get('page', 1))  # 当前页
        limit = int(request.GET.get('limit', 10))  # 每页限定数据数量
        paginator = Paginator(pr_list, limit)  # 分页器
        page = paginator.page(p)  # 当前页数据
        data = {
            'product_search': search_word,
            'pr_list': page.object_list,
            'product_classify': p_classify,
            'product_supplier': p_supplier,
            'paginator': page,
            'total_count': total_count,
        }
        return render(request, "app/product.html", data)
    if request.method == 'POST':
        data = request.POST.dict()
        pr_action = data.get('action')

        if pr_action == "add":

            # 实例化
            pro_classify = Classify.objects.get(id=data.get('classify'))
            pro_supplier = Supplier.objects.get(id=data.get('supplier'))

            pro_num = product_num_id(n=1)  # 生成商品编号
            has_pro_num = Product.objects.filter(pro_num=pro_num)
            while has_pro_num == pro_num:
                pro_num = product_num_id(n=1)

            add_data = {
                'name': data.get('name'),
                'pro_num': pro_num,
                'classify': pro_classify,
                'date_of_manufacture': data.get('date_of_manufacture'),
                'guarantee_period': data.get('guarantee_period'),
                'preserve': u'干燥保存' if data.get('preserve') == '01' else u'低温保存',
                'unit_of_measurement': data.get('uom'),
                'supplier': pro_supplier
            }

            Product.objects.create(**add_data)  # 添加数据
            return write_json({"errno": "0", "msg": "success"})

        elif pr_action == "edit":
            product_id = data.get('product_id')
            tp = Product.objects.get(id=product_id)
            dm = data.get('date_of_manufacture')
            gp = data.get('guarantee_period')

            if dm == '':
                dm = tp.date_of_manufacture
            if gp == '':
                gp = tp.guarantee_period

            edit_data = {
                'name': data.get('name'),
                'classify': data.get('classify'),
                'date_of_manufacture': dm,
                'guarantee_period': gp,
                'preserve': data.get('preserve'),
                'unit_of_measurement': data.get('uom'),
                'supplier': data.get('supplier'),
                'last_update': datetime.datetime.now()
            }
            if product_id:
                Product.objects.filter(id=product_id).update(**edit_data)
                return write_json({"errno": "0", "msg": "success"})
            else:
                return write_json({"errno": "1", "msg": "lost the id!"})

        elif pr_action == "del":
            product_id = data.get('product_id')
            if product_id:
                Product.objects.filter(id=product_id).delete()
                return write_json({"errno": "0", "msg": "success"})
            else:
                return write_json({"errno": "1", "msg": "lost the id!"})
    else:
        return write_json({"errno": "2", "msg": "not action to do!"})


@user_passes_test(lambda u: u.is_staff, login_url='/login')
@permission_required('app.order_manage')
def order(request):
    """订单函数"""
    product_list = Product.objects.all()
    if request.method == "GET":
        order_list = Order.objects.all().order_by('-create_time')
        sw = request.GET.get('order_search', '').strip()

        if sw:
            order_list = Order.objects.filter(order_num=sw)

        total_count = order_list.count()
        p = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))
        paginator = Paginator(order_list, limit)  # 分页器
        page = paginator.page(p)  # 当前页数据

        data = {
            'product_list': product_list,
            'order_list': page.object_list,
            'total_count': total_count,
            'paginator': page,
            'order_search': sw
        }
        return render(request, "app/order.html", data)
    if request.method == "POST":
        data = request.POST.get('pdata')
        tdata = request.POST.dict()
        action = tdata.get('action', '')

        if action == u'add':
            idata = json.loads(data)
            num_id = order_num_id()
            usern = request.user.username
            user = User.objects.get(username=usern)
            # 创建新订单
            Order.objects.create(
                order_num=num_id,
                cost=tdata.get('total_cost', ''),
                order_state=u'01',
                operator=user
            )
            o = Order.objects.last()
            for i in idata:
                num = int(i['num'])
                price = float(i['price'])
                total_price = num * price
                pro = Product.objects.filter(id=int(i['product']))[0]
                # 创建订单商品
                OrderItem.objects.create(
                    product_name=pro,
                    order_number=o,
                    num=num,
                    unit_price=price,
                    total_price=total_price
                )
            return write_json({"errno": 0, "msg": "add success!"})
        elif action == u'del':
            oid = tdata.get('order_id', '')
            if oid:
                OrderItem.objects.filter(order_number__order_num=oid).delete()
                Order.objects.filter(order_num=oid).delete()
                return write_json({"errno": 0, "msg": "delete success!"})
            else:
                return write_json({"errno": 1, "msg": "error! we do not have this order!"})
        elif action == u'edit':
            order_id = tdata.get('order_id', '')
            state = tdata.get('order_state').strip()
            print(state)
            if order_id:
                o = Order.objects.get(order_num=order_id)
                if state == u'未入库':
                    o.order_state = u'04'
                    o.save()
                    return write_json({"errno": 0, "msg": "edit success"})
                else:
                    return write_json({"errno": 2, "msg": "订单状态已为退货状态"})
            else:
                return write_json({"errno": 3, "msg": "没有找到该订单"})


@user_passes_test(lambda u: u.is_staff, login_url='/login')
@permission_required('app.order_manage', raise_exception=True)
def orderitem_list(request):
    """订单商品列表"""
    if request.method == "GET":
        o = request.GET.get('id')
        oid = Order.objects.get(order_num=o)
        oitems = OrderItem.objects.filter(order_number=oid)
        data = {
            'order_items': oitems,
            'order_id': oid.order_num
        }
        return render(request, 'app/order_item_list.html', data)
    pass


@user_passes_test(lambda u: u.is_staff, login_url='/login')
@permission_required('app.warehousing_manage')
def warehousing(request):
    """入库, 方法待改进"""
    if request.method == "GET":
        # 不包含退货的订单都筛选出来并按状态排序
        order_list = Order.objects.filter(order_state=u'01')
        # 获取查询字段
        order_search = request.GET.get('order_search', '')
        if order_search:
            order_list = Order.objects.filter(order_num__contains=order_search, order_state=u'01')
        # 分页器
        p = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))
        paginator = Paginator(order_list, limit)
        page = paginator.page(p)
        data = {
            'order_search': order_search,
            'order_list': page.object_list,
            'paginator': page
        }
        return render(request, 'app/ware_housing.html', data)
    if request.method == 'POST':
        data = request.POST.dict()
        number = data.get('number', '')
        action = data.get('action', '')
        if action == "sin_ware":  # 只有一个订单
            if number:
                # 修改订单状态
                wareorder = Order.objects.get(order_num=number)
                wareorder.order_state = u'02'
                wareorder.save()
                # 查找属于该订单的商品
                op = OrderItem.objects.filter(order_number__order_num=number)
                num = 0
                for p in op:
                    num += 1
                    wnum = str(number) + str(num)
                    lasttime = datetime.datetime.now()
                    # 入库
                    print(p.product_name.pro_num)
                    pr = Product.objects.get(pro_num=p.product_name.pro_num)
                    Warehousing.objects.create(
                        ware_num=wnum,
                        product=pr,
                        last_time=lasttime,
                        remark=number
                    )

                    # 获取最新创建的入库商品,前提是以id排序好的
                    wh = Warehousing.objects.last()

                    # 录入库存
                    Reserve.objects.create(
                        reserve_id=product_num_id(n=2),
                        warenum=wh,
                        product=pr,
                        reserve_num=p.num,
                        last_time=lasttime
                    )
                return write_json({"errno": '0', "msg": "success!"})
            else:
                return write_json({"error": '1', "msg": "找不到该订单!"})
        elif action == "wares":  # 一个或多个订单
            odata = request.POST.get("orderlist")  # 获取数据
            orderlist = json.loads(odata)  # json格式化数据
            for ol in orderlist:
                # 改变订单状态
                o = Order.objects.get(id=ol)
                o.order_state = u'02'
                o.save()
                # 订单商品入库
                op = OrderItem.objects.filter(order_number=o)
                number = o.order_num
                num = 0
                for p in op:
                    num += 1
                    wnum = str(number) + str(num)  # 入库编号
                    lasttime = datetime.datetime.now()  # 最后更新时间
                    # 入库
                    pr = Product.objects.get(pro_num=p.product_name.pro_num)
                    Warehousing.objects.create(
                        ware_num=wnum,
                        product=pr,
                        last_time=lasttime,
                        remark=number
                    )

                    # 获取最新创建的入库商品,前提是以id排序好的(该获取方法可改进)
                    wh = Warehousing.objects.last()

                    # 录入库存
                    Reserve.objects.create(
                        reserve_id=product_num_id(n=2),
                        warenum=wh,
                        product=pr,
                        reserve_num=p.num,
                        last_time=lasttime
                    )
            return write_json({"errno": '0', "msg": "success!"})
        else:
            return write_json({"errno": '1', "msg": "无操作指令"})


@user_passes_test(lambda u: u.is_staff, login_url='/login')
@permission_required('app.reserve_manage')
def reserve(request):
    """库存功能"""
    if request.method == 'GET':
        res_list = Reserve.objects.exclude(reserve_num=0)
        total_count = res_list.count()
        res_search = request.GET.get('res_search', '')
        if res_search:
            res_list = Reserve.objects.filter(
                Q(reserve_id=res_search) |
                Q(warenum__ware_num=res_search) |
                Q(product__name__contains=res_search)
            )

        """
        分页
        1.获取当前页
        2.设置每页数据数量
        3.定义分页器
        4.获取当前页数据
        """
        p = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))
        paginator = Paginator(res_list, limit)
        page = paginator.page(p)

        data = {
            'res_list': page.object_list,
            'res_search': res_search,
            'total_count': total_count,
            'paginator': page
        }
        return render(request, 'app/reserve.html', data)


@user_passes_test(lambda u: u.is_staff, login_url='/login')
@permission_required('app.exwarehousing_manage')
def exwarehousing(request):
    """已出库商品查询页"""
    if request.method == 'GET':
        # 已出库商品
        product_search = request.GET.get('product_search', '')
        delivery_list = ExWareHousing.objects.all().order_by('-id')
        sq = Q(ex_ware_num=product_search) | Q(ex_product__name__contains=product_search)
        if product_search:
            delivery_list = ExWareHousing.objects.filter(sq)
        p = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))
        paginator = Paginator(delivery_list, limit)
        page = paginator.page(p)
        data = {
            'delivery_list': page.object_list,
            'paginator': page,
            'product_search': product_search,
        }
        return render(request, 'app/ex_ware_housing.html', data)


@user_passes_test(lambda u: u.is_staff, login_url='/login')
@permission_required('app.exwarehousing_manage')
def exwareoperate(request):
    """出库功能"""
    # 库存商品
    if request.method == 'GET':
        reserve_list = Reserve.objects.exclude(reserve_num=0)
        p = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))
        paginator = Paginator(reserve_list, limit)
        page = paginator.page(p)
        data = {
            'reserve_list': page.object_list,
            'paginator': page,
        }
        return render(request, 'app/ex_ware_operate.html', data)

    if request.method == 'POST':
        data = request.POST.get('product_data', '')
        tdata = request.POST.dict()
        action = tdata.get('action', '')
        if action == "delivery":
            res_id = tdata.get('reserve_id', '')
            number = int(tdata.get('number', ''))
            try:
                res = Reserve.objects.get(reserve_id=res_id)
            except ValueError as e:
                return write_json({"error": '3', "msg": e})

            if res:
                res_num = res.reserve_num
                if number <= res_num:
                    res_num = res_num - number
                    # 改变库存数量并保存
                    res.reserve_num = res_num
                    res.save()
                    # 新增出库商品数据
                    ex_ware_num = product_num_id(3)
                    pro = Product.objects.get(id=res.product_id)
                    # 商品出库
                    ExWareHousing.objects.create(
                        ex_ware_num=ex_ware_num,
                        ex_product=pro,
                        ex_reserve=res,
                        out_num=number
                    )
                    return write_json({"errno": '0', "msg": "success"})
                elif number > res_num:
                    return write_json({'errno': '2', 'msg': "库存不足!"})
            else:
                return write_json({"errno": '4', 'msg': "找不到该库存!"})
        elif action == 'all_delivery':
            product_data = json.loads(data)
            for pd in product_data:
                res_id = pd['reserve_id']
                num = int(pd['num'])
                res = Reserve.objects.get(reserve_id=res_id)
                if res:
                    res_num = res.reserve_num
                    if num <= res_num:
                        res_num = res_num - num
                        # 改变库存数量并保存
                        res.reserve_num = res_num
                        res.save()
                        # 新增出库商品数据
                        ex_ware_num = product_num_id(3)
                        pro = Product.objects.get(id=res.product_id)
                        # 商品出库
                        ExWareHousing.objects.create(
                            ex_ware_num=ex_ware_num,
                            ex_product=pro,
                            ex_reserve=res,
                            out_num=num
                        )
                    elif num > res_num:
                        return write_json({'errno': '2', 'msg': "库存不足!"})
                else:
                    return write_json({"errno": '4', 'msg': "找不到该库存!"})
            return write_json({'errno': '0', "msg": "success"})
        else:
            return write_json({"errno": '1', "msg": "have no action to do!"})


@user_passes_test(lambda u: u.is_staff, login_url='/login')
@permission_required('app.employee_manage')
def employee_list(request):
    """员工列表"""
    if request.method == 'GET':
        del_id = request.GET.get('id', False)
        employee_search = request.GET.get('employee_search', '')
        user_list = User.objects.filter(is_staff=True, is_active=True, is_superuser=False)
        if employee_search:
            user_list = User.objects.filter(
                is_staff=True,
                is_active=True,
                is_superuser=False,
                username__contains=employee_search
            )
        pos_list = []
        for u in user_list:
            u_list = []
            perms = u.get_all_permissions()
            for p in perms:
                code = p[4:len(p)]
                perm = Permission.objects.get(codename=code)
                u_list.append(perm.name)
            pos_list.append([u, u_list])

        if del_id:
            user = User.objects.get(id=del_id)
            if not user:
                return redirect('/operate/tips')
            user.is_active = False
            user.save()
            return redirect('/employee/list')

        data = {
            'user_list': pos_list,
            'employee_search': employee_search,
        }
        return render(request, 'app/employee_list.html', data)


@user_passes_test(lambda u: u.is_staff, login_url='/login')
@permission_required('app.employee_manage')
def employee_operate(request):
    """增加员工"""

    # 将自定义的权限放入字典中
    perm_dict = dict((x, y) for x, y in PERMS)

    if request.method == 'GET':
        data = {
            'perm': perm_dict,
        }
        return render(request, 'app/employee_operate.html', data)

    if request.method == 'POST':
        perm_list = []
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        e_mail = request.POST.get('email', '')
        psd = request.POST.get('password', '')
        check = request.POST.getlist('check', '')
        position = request.POST.get('position', '')
        print('姓名: '+name+', 电话: '+phone+', 邮箱: '+e_mail+', 密码: '+psd)
        print(check)

        if not check:
            # 重定向到提示页面
            return redirect('/operate/tips?msg=' + u'未给该工作人员添加操作权限')

        for code in check:
            # 赋予权限
            content_type = ContentType.objects.get_for_model(Employee)
            perm, created = Permission.objects.update_or_create(
                codename=code,
                name=perm_dict[code],
                content_type=content_type
            )
            # 将权限放到数组中
            perm_list.append(perm)

        username = User.objects.filter(username=name)
        if username:
            return redirect('/operate/tips?msg=' + u'工作人员已存在')

        # 创建用户
        user = User.objects.create_user(
            username=name,
            email=e_mail,
            password=psd,
            is_staff=True
        )
        Employee.objects.create(
            user=user,
            name=name,
            phone=phone,
            position=position
        )

        user = authenticate(username=name, password=psd)
        user.user_permissions.set(perm_list)

        data = {
            'data': u'工作人员创建成功!',
            'perm': perm_dict
        }

        return render(request, 'app/employee_operate.html', data)


@user_passes_test(lambda u: u.is_staff, login_url='/login')
@permission_required('app.employee_manage')
def employee_detail(request):
    """工作人员信息详情/修改"""
    perm_dict = dict((x, y) for x, y in PERMS)
    if request.method == 'GET':
        e_id = request.GET.get('id', False)
        if not e_id:
            return redirect('/operate/tips?msg=' + u'无此用户')
        uemp = User.objects.get(is_staff=True, is_superuser=False, id=e_id)
        pos_dict = {}
        perms = uemp.get_all_permissions()
        for p in perms:
            code = p[4:len(p)]  # 仅需要权限名称, 所以只节选到权限名称的第一个字母的位置
            perm = Permission.objects.get(codename=code)
            pos_dict[perm.codename] = perm.name

        data = {
            'perm': perm_dict,
            'user': uemp,
            'pos': pos_dict
        }
        return render(request, 'app/employee_detail.html', data)

    if request.method == 'POST':
        e_id = request.POST.get('id', '')
        if not e_id:
            return redirect('/operate/tips?msg=' + u'无此用户')
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        position = request.POST.get('position', '')
        psd = request.POST.get('password', '')
        check = request.POST.getlist('check', '')

        try:
            user = User.objects.get(is_staff=True, is_superuser=False, id=e_id)
            emp = Employee.objects.get(user=user)
            user.username = name
            user.email = email
            emp.name = name
            emp.phone = phone
            emp.position = position
            if psd:
                user.set_password(psd)
            user.save()
            emp.save()
        except Exception as e:
            return redirect('/operate/tips?msg=' + e)

        # 权限修改
        p_list = []
        perm_s = ''
        for code in check:
            content_type = ContentType.objects.get_for_model(Employee)
            perms = Permission.objects.filter(codename=code)
            if perms.count() == 0:
                perm, created = Permission.objects.update_or_create(
                    codename=code,
                    name=perm_dict[code],
                    content_type=content_type
                )
            else:
                perm = perms[0]

            p_list.append(perm)
            perm_s += '%s' % perm_dict[code]
        user.user_permissions.clear()
        user.user_permissions.set(p_list)
        return redirect('/employee/list')


def operate_tip(request):
    """异常提示"""
    msg = request.GET.get('msg', u'数据操作异常')
    data = {
        'msg': msg,
    }
    return render(request, 'app/tips.html', data)
