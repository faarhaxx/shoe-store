from django.contrib import admin
from django.contrib import admin
from .models import Product

admin.site.register(Product)
from django.contrib import admin
from .models import Order, OrderItem

admin.site.register(Order)
admin.site.register(OrderItem)

from django.contrib import admin
from .models import Order

try:
    admin.site.unregister(Order)
except:
    pass

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'total_amount', 'status']

admin.site.register(Order, OrderAdmin)
# Register your models here.
