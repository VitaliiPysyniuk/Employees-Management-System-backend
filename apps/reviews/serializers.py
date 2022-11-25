from rest_framework.serializers import ModelSerializer

from .models import ReviewModel


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = ReviewModel
        fields = '__all__'
