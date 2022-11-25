from django.urls import path, include

urlpatterns = [
    path('/users', include('apps.users.urls')),
    path('/reviews', include('apps.reviews.urls')),
    path('/quizzes', include('apps.quizzes.urls'))
]
