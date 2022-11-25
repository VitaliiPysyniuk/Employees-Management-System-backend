from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

from .models import ReviewModel
from .serializers import ReviewSerializer
from apps.users.permissions import IsAdmin

UserModel = get_user_model()


class ReviewListCreateView(ListCreateAPIView):
    serializer_class = ReviewSerializer

    def create(self, request, *args, **kwargs):
        request.data['creator'] = request.user.id
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.user.role == UserModel.Role.EMPLOYEE:
            return ReviewModel.objects.filter(employee=self.request.user.id)
        return ReviewModel.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAdmin()]


class ReviewRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    lookup_field = 'id'

    def get_queryset(self):
        if self.request.user.role == UserModel.Role.EMPLOYEE:
            return ReviewModel.objects.filter(employee=self.request.user.id)
        return ReviewModel.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAdmin()]






