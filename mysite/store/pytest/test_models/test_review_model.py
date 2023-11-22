# class Review(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
#     rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
#     comment = models.TextField(blank=True, null=True)
#     review_date = models.DateTimeField(default=timezone.now)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"Review for {self.product.name} by {self.user.user.username} - Rating: {self.rating}"

#     class Meta:
#         ordering = ['-review_date']
#         unique_together = ['product', 'user']
#         verbose_name_plural = 'Reviews'
#   """

from store.models import Review
import pytest


@pytest.mark.django_db
def test_review_model(new_user_profile, test_product):
    """ Test Review model """
    user= new_user_profile('testuser')
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
