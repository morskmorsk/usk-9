import pytest
from django.utils import timezone
from store.models import Supplier
from phonenumber_field.modelfields import PhoneNumberField

@pytest.mark.django_db
def test_create_supplier():
    supplier_name = "Global Tech"
    supplier_phone = '+1234567890'
    supplier_address = "456 Tech Street"
    supplier_city = "Innovate City"
    supplier_state = "TS"
    supplier_zip = "12345"
    supplier_email = "contact@globaltech.com"
    supplier_website = "https://www.globaltech.com"
    supplier_contact_person = "John Doe"
    supplier_type = "Electronics"
    supplier_notes = "Leading supplier in tech."

    supplier = Supplier.objects.create(
        name=supplier_name,
        phone=supplier_phone,
        address=supplier_address,
        city=supplier_city,
        state=supplier_state,
        zip_code=supplier_zip,
        email=supplier_email,
        website=supplier_website,
        contact_person=supplier_contact_person,
        type=supplier_type,
        notes=supplier_notes
    )

    assert supplier.name == supplier_name
    assert supplier.phone == supplier_phone
    assert supplier.address == supplier_address
    assert supplier.city == supplier_city
    assert supplier.state == supplier_state
    assert supplier.zip_code == supplier_zip
    assert supplier.email == supplier_email
    assert supplier.website == supplier_website
    assert supplier.contact_person == supplier_contact_person
    assert supplier.type == supplier_type
    assert supplier.notes == supplier_notes
    assert supplier.created_at <= timezone.now()
    assert supplier.updated_at <= timezone.now()

@pytest.mark.django_db
def test_supplier_str():
    supplier = Supplier.objects.create(name="Tech Supplies", contact_info="info@techsupplies.com")
    expected_str = "Tech Supplies - Contact: info@techsupplies.com"
    
    assert str(supplier) == expected_str

@pytest.mark.django_db
def test_supplier_blank_fields():
    supplier = Supplier.objects.create(name="Basic Supplies", zip_code="12345")  # Minimal required fields

    assert supplier.phone is None or supplier.phone == ''
    assert supplier.address is None
    assert supplier.city is None
    assert supplier.state is None
    assert supplier.email is None
    assert supplier.website is None
    assert supplier.contact_person is None
    assert supplier.type is None
    assert supplier.notes is None
