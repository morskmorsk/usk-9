import pytest
from decimal import Decimal
from store.models import WorkOrder
from django.utils import timezone

# test work order creation
@pytest.mark.django_db
def test_work_order_creation(test_user):
    work_order_created_at = timezone.now()
    work_order_updated_at = timezone.now()
    user=test_user('workordertestuser')
    work_order = WorkOrder.objects.create(
        user=user,
        status='pending',
        notes='Test notes',
        assigned_to=None,
        estimated_completion_date=None,
        actual_completion_date=None,
        created_at=work_order_created_at,
        updated_at=work_order_updated_at,
    )
    assert work_order.id == 1
    assert work_order.user == user
    assert work_order.status == 'pending'
    assert work_order.notes == 'Test notes'
    assert work_order.assigned_to == None
    assert work_order.estimated_completion_date == None
    assert work_order.actual_completion_date == None
    assert str(work_order) == f"Work Order {work_order.id} - Status: {work_order.get_status_display()}"
    
