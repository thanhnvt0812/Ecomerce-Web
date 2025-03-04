from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
# Register your models here.
#register models on admin section thing
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

#create order item inline => order + orderitem to view all shipping info
class OrderItemInline(admin.StackedInline):
    model= OrderItem
    extra = 0

#extend order model
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ["date_ordered"]
    inlines = [OrderItemInline]

#unregister order model 
admin.site.unregister(Order)
#re-register order and orderitem
admin.site.register(Order, OrderAdmin)
