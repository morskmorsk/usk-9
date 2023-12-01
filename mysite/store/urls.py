from django.urls import path
from .views import (ProductListView,
                    ProductDetailView,
                    AddToCartView,
                    ShoppingCartView,
                    RemoveFromCartDetailView,
                    CartDetailUpdatePriceView,
                    CheckOutView,
                    UpdateUserProfileView,
                    AddDeviceView
                    )

urlpatterns = [
     path('', ProductListView.as_view(), name='home'),
     path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
     path('add-to-cart/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
     path('cart/', ShoppingCartView.as_view(), name='cart'),
     path('remove-from-cart/<int:detail_id>/', RemoveFromCartDetailView.as_view(), name='remove_from_cart'),
     path('cart-detail/<int:detail_id>/', CartDetailUpdatePriceView.as_view(), name='update-cart-detail-price'),
     path('checkout/', CheckOutView.as_view(), name='checkout'),
     path('update-profile/', UpdateUserProfileView.as_view(), name='update-profile'),
     path('add-device/', AddDeviceView.as_view(), name='add-device'),
     # path('cart-form', CartDetailFormView.as_view(), name='cart-form',),
     # path('add-to-cart/<int:id>/', AddToCartView.as_view(), name='add-to-cart'),
     # path('shopping-cart/', ShoppingCartListView.as_view(), name='shopping-cart-list'),
     # path('checkout/', CheckOutView.as_view(), name='checkout'),
     # path('new-work-order/', NewWorkOrderView.as_view(), name='new-work-order'),
     # # path('products/<int:id>/addtocart/', AddToCartView.as_view(), name='add-to-cart'),
     # path('add-to-cart/<int:id>/', AddToCartView.as_view(), name='add-to-cart'),
     # path('workorders/', WorkOrderListView.as_view(), name='work-orders-list'),
     # path('cart-form/<int:id>/', CartFormView.as_view(), name='cart-form'),
]
