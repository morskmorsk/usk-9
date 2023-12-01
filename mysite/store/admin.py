from django.contrib import admin
from .models import (Department,
                     Location,
                     Supplier,
                     Product,
                     Order,
                     OrderDetail,
                     Review,
                     ShoppingCart,
                     ShoppingCartDetail,
                     WorkOrder,
                     Part,
                     Device,
                     )


admin.site.register(Department)
admin.site.register(Location)
admin.site.register(Supplier)
admin.site.register(Device)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(Part)
admin.site.register(Review)
admin.site.register(ShoppingCart)
admin.site.register(ShoppingCartDetail)
admin.site.register(WorkOrder)
