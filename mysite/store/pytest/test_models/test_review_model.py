# class Review(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
#     comment = models.TextField(blank=True, null=True)
#     review_date = models.DateTimeField(default=timezone.now)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"Review for {self.product.name} by {self.user.user.username} - Rating: {self.rating}"
    
#     class Meta:
#         ordering = ['-review_date']
#         unique_together = ['product', 'user']
#         verbose_name_plural = 'Reviews'
import pytest
from store.models import Review

@pytest.mark.django_db
def test_review_model(test_product, test_user):
    review = Review.objects.create(
        product=test_product,
        user=test_user('testuser'),
        rating=5,
        comment='Test Review Comment',
    )
    assert review.product == test_product
    assert review.user.username == 'testuser'
    assert review.rating == 5
    assert review.comment == 'Test Review Comment'
