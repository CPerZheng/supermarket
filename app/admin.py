from django.contrib import admin
from app.models import Classify, Supplier, Employee, Product, Order, OrderItem, Warehousing, ExWareHousing


# Register your models here.
admin.site.register(Classify)
admin.site.register(Supplier)
admin.site.register(Employee)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Warehousing)
admin.site.register(ExWareHousing)
