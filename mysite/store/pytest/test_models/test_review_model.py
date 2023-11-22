from store.models import Review
import pytest


@pytest.mark.django_db
def test_review_model(test_user, test_product):
    """ Test Review model """
    user= test_user('testuser')
    review = Review.objects.create(
        product=test_product,
        user=user,
        rating=5,
        comment='Test comment',
    )
    assert review.product == test_product
    assert review.user == user
    assert review.rating == 5
    assert review.comment == 'Test comment'
