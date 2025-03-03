from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem
# Register your models here.
#register models on admin section thing
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

