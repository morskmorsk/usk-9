from django.contrib import admin
from .models import (Department, Category, Location, Supplier, DeviceDefect, Device_IMEI,
                     DeviceManufacturer, DeviceStatus, DeviceGrade, DeviceModel, Product,
                     ProductSupplier, Payment, Order, OrderDetail, Return, Inventory,
                     Review, ShoppingCart, ShoppingCartDetail,Payment,
                     WorkOrder, Service, Part, ServiceDetail,WorkOrderDetail, Device
                     )


admin.site.register(Department)
admin.site.register(Category)
admin.site.register(Location)
admin.site.register(Supplier)
admin.site.register(DeviceDefect)
admin.site.register(Device_IMEI)
admin.site.register(DeviceManufacturer)
admin.site.register(DeviceStatus)
admin.site.register(DeviceGrade)
admin.site.register(DeviceModel)
admin.site.register(Device)
admin.site.register(Product)
admin.site.register(ProductSupplier)
admin.site.register(Inventory)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(Service)
admin.site.register(ServiceDetail)
admin.site.register(Part)
admin.site.register(Payment)
admin.site.register(Review)
admin.site.register(Return)
admin.site.register(ShoppingCart)
admin.site.register(ShoppingCartDetail)
admin.site.register(WorkOrder)
admin.site.register(WorkOrderDetail)
