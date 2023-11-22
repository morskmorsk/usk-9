from django.urls import path
from .views import (ProductListView, ProductDetailView)

urlpatterns = [
     path('', ProductListView.as_view(), name='home'),
     path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
     # path('shopping-cart/', ShoppingCartListView.as_view(), name='shopping-cart-list'),
     # path('checkout/', CheckOutView.as_view(), name='checkout'),
     # path('new-work-order/', NewWorkOrderView.as_view(), name='new-work-order'),
     # # path('products/<int:id>/addtocart/', AddToCartView.as_view(), name='add-to-cart'),
     # path('add-to-cart/<int:id>/', AddToCartView.as_view(), name='add-to-cart'),
     # path('workorders/', WorkOrderListView.as_view(), name='work-orders-list'),
     # path('cart-form/<int:id>/', CartFormView.as_view(), name='cart-form'),
]
