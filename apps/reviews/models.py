from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class ReviewModel(models.Model):
    class Meta:
        db_table = 'reviews'

    title = models.CharField(max_length=60)
    description = models.CharField(max_length=200, blank=True)
    position_before = models.CharField(max_length=60, blank=True)
    position_after = models.CharField(max_length=60, blank=True)
    salary_change = models.IntegerField(default=0)
    review_date = models.DateField()

    employee = models.ForeignKey(UserModel, on_delete=models.PROTECT, related_name='reviews')
    creator = models.ForeignKey(UserModel, on_delete=models.PROTECT, related_name='created_reviews')
