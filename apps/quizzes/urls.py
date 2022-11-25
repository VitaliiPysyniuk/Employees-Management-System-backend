from django.urls import path

from .views import CategoryListCreateView, CategoryRetrieveUpdateDestroyView, QuestionListCreateView, \
    QuestionRetrieveUpdateDestroyView, QuizListCreateView, QuizRetrieveUpdateDestroyView, QuizResultListCreateView

urlpatterns = [
    path('', QuizListCreateView.as_view(), name='get_create_quizzes'),
    path('/<int:id>', QuizRetrieveUpdateDestroyView.as_view(), name='get_update_delete_single_quiz'),
    path('/results', QuizResultListCreateView.as_view(), name='get_create_quiz_result'),
    path('/questions', QuestionListCreateView.as_view(), name='get_create_questions'),
    path('/questions/<int:id>', QuestionRetrieveUpdateDestroyView.as_view(), name='get_update_delete_single_question'),
    path('/categories', CategoryListCreateView.as_view(), name='get_create_categories'),
    path('/categories/<int:id>', CategoryRetrieveUpdateDestroyView.as_view(), name='get_update_delete_single_category')
]