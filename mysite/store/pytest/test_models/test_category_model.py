import pytest
from django.utils import timezone
from store.models import Category
from django.core.files.uploadedfile import SimpleUploadedFile

@pytest.mark.django_db
def test_create_category():
    category_name = "Electronics"
    category_description = "Gadgets and electronic devices"
    category_image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")

    category = Category.objects.create(
        name=category_name,
        description=category_description,
        image=category_image
    )

    assert category.name == category_name
    assert category.description == category_description
    assert category.image  # Check if image is uploaded
    assert category.created_at <= timezone.now()
    assert category.updated_at <= timezone.now()

@pytest.mark.django_db
def test_category_str():
    category = Category.objects.create(name="Books")
    created_at_str = category.created_at.strftime('%Y-%m-%d')
    expected_str = f"Books (Added on {created_at_str})"
    
    assert str(category) == expected_str

@pytest.mark.django_db
def test_category_default_values():
    category = Category.objects.create(name="Apparel")

    assert category.description is None
    # Correctly handle the empty ImageField
    assert not category.image
