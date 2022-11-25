from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.contrib.auth import get_user_model

from .serializers import UserSerializer
from ..reviews.serializers import ReviewSerializer
from ..reviews.models import ReviewModel
from .permissions import IsAdmin

UserModel = get_user_model()


class UserListCreateView(ListCreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]


class UserRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
    permission_classes = [IsAdmin]

    def perform_destroy(self, instance):
        serializer = self.get_serializer(instance, data={'is_active': False}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()


class UserReviewsListView(ListAPIView):
    queryset = ReviewModel.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'employee'
    permission_classes = [IsAdmin]






