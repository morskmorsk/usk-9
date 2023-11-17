import pytest
from django.utils import timezone
from store.models import Department

@pytest.mark.django_db
def test_create_department():
    department_name = "Finance"
    department_description = "Handles financial matters"
    
    department = Department.objects.create(
        name=department_name,
        description=department_description,
        taxable=True
    )

    assert department.name == department_name
    assert department.description == department_description
    assert department.taxable is True
    assert department.created_at <= timezone.now()
    assert department.updated_at <= timezone.now()

@pytest.mark.django_db
def test_department_str():
    department = Department.objects.create(name="HR")
    created_at_str = department.created_at.strftime('%Y-%m-%d')
    expected_str = f"HR (Created on {created_at_str})"
    
    assert str(department) == expected_str

@pytest.mark.django_db
def test_department_default_values():
    department = Department.objects.create(name="IT")

    assert department.description is None
    assert department.taxable is True  # Default value
