import random
from typing import Any
import uuid
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView, TemplateView
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
import logging
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .forms import UserForm
from django.contrib.auth import login
from django.views import View
from .models import Device, Product, ShoppingCart, ShoppingCartDetail, WorkOrder
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.db import IntegrityError, models, transaction
from django.contrib import messages
from django.contrib.auth.models import User

from .models import Product

logger = logging.getLogger(__name__)


class ProductListView(LoginRequiredMixin,ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'products'

    class Meta:
        ordering = ['-id']
        plural_name = 'Products'


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'store/product_detail.html'
    context_object_name = 'product'


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = UserForm
    success_url = reverse_lazy('home')  # Redirect to home or another appropriate page

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)  # Log in the user immediately after signup
        cart, created = ShoppingCart.objects.get_or_create(user=user)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return super().form_invalid(form)


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            product = get_object_or_404(Product, id=kwargs.get('product_id'))
            with transaction.atomic():
                cart, created = ShoppingCart.objects.get_or_create(user=request.user)
                cart_detail = ShoppingCartDetail.objects.create(
                    cart=cart,
                    product=product,
                    price=request.POST.get('price'),
                    quantity=1
                )
                cart_detail.save()
        except IntegrityError as e:
            messages.error(request, f"Error adding product to cart: {e}")
            # Redirect to the previous page or a specific error page
            return redirect(request.META.get('HTTP_REFERER', 'product-detail'), product_id=product.id)
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {e}")
            # Redirect to an error page or home page
            return redirect('home')

        return redirect('cart')
    

class ShoppingCartView(LoginRequiredMixin, DetailView):
    model = ShoppingCart
    template_name = 'store/shopping_cart_list.html'  # replace with your actual template path

    def get_object(self, queryset=None):
        return ShoppingCart.objects.get(user=self.request.user)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.get_object()
        context['cart'] = {
            'subtotal': cart.calculate_subtotal(),
            'tax': cart.calculate_tax(),
            'total': cart.calculate_total(),
        }
        return context


class RemoveFromCartDetailView(LoginRequiredMixin, DeleteView):
    def post(self, request, *args, **kwargs):
        cart_detail = get_object_or_404(ShoppingCartDetail, id=kwargs.get('detail_id'))
        cart_detail.delete()
        return redirect('cart')
    

class CartDetailUpdatePriceView(LoginRequiredMixin, UpdateView):
    model = ShoppingCartDetail
    fields = ['price']
    template_name = 'store/cart_detail_update.html'
    success_url = reverse_lazy('cart')

    def get_object(self, queryset=None):
        return ShoppingCartDetail.objects.get(id=self.kwargs.get('detail_id'))


class CheckOutView(LoginRequiredMixin, TemplateView):
    template_name = 'store/checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = ShoppingCart.objects.get(user=self.request.user)
        context['cart'] = {
            'subtotal': cart.calculate_subtotal(),
            'tax': cart.calculate_tax(),
            'total': cart.calculate_total(),
            'change_due': cart.calculate_total() * -1,
        }
        return context


class UpdateUserProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = 'store/user_profile_update.html'
    success_url = reverse_lazy('home')
    success_message = 'Profile successfully updated!'

    def get_object(self, queryset=None):
        return self.request.user


class AddDeviceView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Device
    fields = ['name', 'price', 'description', 'issues', 'grade', 'cost', 'imei', 'supplier', 'location', 'image', 'defect', 'color']
    template_name = 'store/add_device.html'
    success_url = reverse_lazy('home')
    success_message = 'Device successfully added!'

    def form_valid(self, form):
        # Generate a random 15-digit number
        fifteen_digit_uuid = random.randint(100000000000000, 999999999999999)
        form.instance.sku = fifteen_digit_uuid
        form.instance.owner = self.request.user

        # Save the Device instance
        response = super().form_valid(form)

        # Create a WorkOrder for the newly created Device
        WorkOrder.objects.create(
            user=self.request.user,
            device=form.instance,
            description='New device added to inventory.',
            problem='New device added to inventory.',
            notes='New device added to inventory.',
        )
        return response

    def form_invalid(self, form):
        return super().form_invalid(form)


class DeviceListView(LoginRequiredMixin, ListView):
    model = Device
    template_name = 'store/device_list.html'
    context_object_name = 'devices'

    def get_queryset(self):
        return Device.objects.filter(owner=self.request.user)

    class Meta:
        ordering = ['id']
        plural_name = 'Devices'


class WorkOrderListView(LoginRequiredMixin, ListView):
    model = WorkOrder
    template_name = 'store/work_order_list.html'
    context_object_name = 'work_orders'

    def get_queryset(self):
        return WorkOrder.objects.filter(user=self.request.user)
            
    class Meta:
        ordering = ['id']
        plural_name = 'Work Orders'


class WorkOrderDetailView(LoginRequiredMixin, DetailView):
    model = WorkOrder
    template_name = 'store/work_order_detail.html'
    context_object_name = 'work_order'


class DeviceDetailView(LoginRequiredMixin, DetailView):
    model = Device
    template_name = 'store/device_detail.html'
    context_object_name = 'device'


class DeviceUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Device
    fields = ['name', 'price', 'description', 'issues', 'grade', 'cost', 'imei', 'supplier', 'location', 'image', 'defect', 'color']
    template_name = 'store/device_update.html'
    success_url = reverse_lazy('device-list')
    success_message = 'Device successfully updated!'

    def get_object(self, queryset=None):
        return Device.objects.get(id=self.kwargs.get('device_id'))


class WorkOrderUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = WorkOrder
    fields = ['description', 'problem', 'notes', 'status', 'assigned_to', 'estimated_completion_date', 'actual_completion_date']
    template_name = 'store/work_order_update.html'
    success_url = reverse_lazy('work-orders-list')
    success_message = 'Work Order successfully updated!'

    def get_object(self, queryset=None):
        return WorkOrder.objects.get(id=self.kwargs.get('work_order_id'))