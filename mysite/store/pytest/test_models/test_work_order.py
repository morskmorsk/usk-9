# class WorkOrder(models.Model):
#     customer = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     status = models.CharField(max_length=20, choices=WORK_ORDER_STATUS_CHOICES, default='pending')
#     assigned_to = models.ForeignKey(UserProfile, related_name='assigned_orders', on_delete=models.SET_NULL, null=True, blank=True)
#     notes = models.TextField(blank=True, null=True)
#     estimated_completion_date = models.DateTimeField(blank=True, null=True)
#     actual_completion_date = models.DateTimeField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)


#     def __str__(self):
#         return f"Work Order {self.id} - Status: {self.get_status_display()}"

import pytest
from decimal import Decimal
from store.models import WorkOrder
from django.utils import timezone

# test work order creation
@pytest.mark.django_db
def test_work_order_creation(new_user_profile):
    work_order_created_at = timezone.now()
    work_order_updated_at = timezone.now()
    user=new_user_profile('workordertestuser')
    work_order = WorkOrder.objects.create(
        customer=user,
        status='pending',
        notes='Test notes',
        assigned_to=None,
        estimated_completion_date=None,
        actual_completion_date=None,
        created_at=work_order_created_at,
        updated_at=work_order_updated_at,
    )
    assert work_order.id == 1
    assert work_order.customer == user
    assert work_order.status == 'pending'
    assert work_order.notes == 'Test notes'
    assert work_order.assigned_to == None
    assert work_order.estimated_completion_date == None
    assert work_order.actual_completion_date == None
    # assert work_order.created_at == work_order_created_at
    # assert work_order.updated_at == work_order_updated_at
    assert str(work_order) == f"Work Order {work_order.id} - Status: {work_order.get_status_display()}"
    
