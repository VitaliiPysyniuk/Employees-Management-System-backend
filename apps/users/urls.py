from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserListCreateView, UserRetrieveUpdateDestroyView, UserReviewsListView

urlpatterns = [
    path('', UserListCreateView.as_view(), name='get_create_users'),
    path('/<int:id>', UserRetrieveUpdateDestroyView.as_view(), name='get_update_delete_single_user'),
    path('/<int:id>/reviews', UserReviewsListView.as_view(), name='get_all_users_reviews'),
    path('/login', TokenObtainPairView.as_view(), name='login_user'),
    path('/refresh', TokenRefreshView.as_view(), name='refresh_access_token')
]
