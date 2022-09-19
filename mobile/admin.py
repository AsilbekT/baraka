from django.contrib import admin
from mobile.models import (
    Catagory, 
    Product, 
    Order, 
    OrderItem, 
    ShippingAddress,
    MainCatagory
    )

# Register your models here.
admin.site.register(MainCatagory)
admin.site.register(Catagory)

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)

