from django.urls import path
from .views import (ProductListView,
                    ProductDetailView,
                    AddToCartView,
                    ShoppingCartView,
                    RemoveFromCartDetailView,
                    CartDetailUpdatePriceView,
                    CheckoutView,
                    UpdateUserProfileView,
                    AddDeviceView,
                    DeviceListView,
                    WorkOrderListView,
                    WorkOrderDetailView,
                    DeviceDetailView,
                    DeviceUpdateView,
                    WorkOrderUpdateView,
                    ClearPaymentsView
                    )
from django.urls import path
from .views import CashPaymentView, CardPaymentView

urlpatterns = [
     path('', ProductListView.as_view(), name='home'),
     path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
     path('add-to-cart/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
     path('cart/', ShoppingCartView.as_view(), name='cart'),
     path('remove-from-cart/<int:detail_id>/', RemoveFromCartDetailView.as_view(), name='remove_from_cart'),
     path('cart-detail/<int:detail_id>/', CartDetailUpdatePriceView.as_view(), name='update-cart-detail-price'),
     path('checkout/', CheckoutView.as_view(), name='checkout'),
     path('update-profile/', UpdateUserProfileView.as_view(), name='update-profile'),
     path('add-device/', AddDeviceView.as_view(), name='add-device'),
     path('devices/', DeviceListView.as_view(), name='device-list'),
     path('workorders/', WorkOrderListView.as_view(), name='work-orders-list'),
     path('workorders/<int:pk>/', WorkOrderDetailView.as_view(), name='work-order-detail'),
     path('devices/<int:pk>/', DeviceDetailView.as_view(), name='device-detail'),
     path('devices/<int:device_id>/update/', DeviceUpdateView.as_view(), name='device-update'),
     path('workorders/<int:work_order_id>/update/', WorkOrderUpdateView.as_view(), name='work-order-update'),
     path('save-cash-payment/', CashPaymentView.as_view(), name='save-cash-payment'),
     path('save-credit-payment/', CardPaymentView.as_view(), name='save-credit-payment'),
     path('clear-payments/', ClearPaymentsView.as_view(), name='clear-payments'),
]    
