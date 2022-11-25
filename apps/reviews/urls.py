from django.urls import path

from .views import ReviewListCreateView, ReviewRetrieveUpdateDestroyView

urlpatterns = [
    path('', ReviewListCreateView.as_view(), name='get_create_reviews'),
    path('/<int:id>', ReviewRetrieveUpdateDestroyView.as_view(), name='get_update_delete_single_review')
]
