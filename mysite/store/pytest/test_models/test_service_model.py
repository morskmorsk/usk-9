import pytest
from store.models import Service
from django.utils import timezone


# create test for service model
@pytest.mark.django_db
def test_service_creation(test_work_order, test_user, test_time):
    name = 'Test Service'
    description = 'Test Description'
    work_order = test_work_order
    technician = test_user('testtechnician')
    service_date = test_time
    service = Service.objects.create(
        name=name,
        description=description,
        work_order=work_order,
        technician=technician,
        service_date=service_date,
    )
    assert service.id == 1
    assert service.name == 'Test Service'
    assert service.description == 'Test Description'
    assert service.work_order == work_order
    assert service.technician == technician
    assert str(service) == service.name