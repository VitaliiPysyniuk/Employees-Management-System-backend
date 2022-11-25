from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

from .models import QuizModel, QuizResultModel, QuestionModel, CategoryModel, AnswerModel
from .serializers import QuizResultSerializer, FullQuestionSerializer, ShortQuestionSerializer, \
    CategoryCreateSerializer, CategoryListSerializer, QuizSerializer, FullQuizSerializer, ShortQuizSerializer, \
    QuizForEmployeeSerializer
from apps.users.permissions import IsAdmin
from .services import evaluate_user_answers

UserModel = get_user_model()


class QuizListCreateView(ListCreateAPIView):
    queryset = QuizModel.objects.prefetch_related('questions')

    def create(self, request, *args, **kwargs):
        request.data['creator'] = request.user.id
        return super().create(request, *args, **kwargs)

    def get_serializer_class(self):
        query_params = self.request.query_params
        if self.request.method == 'POST':
            return QuizSerializer
        if (query_params.get('with_questions') and query_params.get('with_questions') == 'False') \
                or (self.request.user.role == UserModel.Role.EMPLOYEE):
            return ShortQuizSerializer
        return FullQuizSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdmin()]
        return [IsAuthenticated()]

    def get_queryset(self):
        query_params = self.request.query_params
        if self.request.method == 'POST':
            return super().get_queryset()
        if (query_params.get('with_questions') and query_params.get('with_questions') == 'False') \
                or (self.request.user.role == UserModel.Role.EMPLOYEE):
            return super().get_queryset()
        return QuizModel.objects.prefetch_related('questions', 'questions__categories', 'questions__answers')


class QuizRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = QuizModel.objects.prefetch_related('questions')
    lookup_field = 'id'

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAdmin()]

    def get_serializer_class(self):
        if self.request.user.role == UserModel.Role.EMPLOYEE:
            return QuizForEmployeeSerializer
        if self.request.method == 'GET':
            return FullQuizSerializer
        return QuizSerializer


class QuizResultListCreateView(ListCreateAPIView):
    serializer_class = QuizResultSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user_answers = request.data.pop('answers', [])
        answers = AnswerModel.objects.filter(question__quizzes__id=request.data.get('quiz')).filter(is_correct=True) \
            .order_by('id')

        data = evaluate_user_answers(user_answers, answers, request)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        if self.request.user.role == UserModel.Role.EMPLOYEE:
            return QuizResultModel.objects.filter(employee=self.request.user.id)
        return QuizResultModel.objects.all()


class QuestionListCreateView(ListCreateAPIView):
    permission_classes = [IsAdmin]

    def get_serializer_class(self):
        with_answers = self.request.query_params.get('with_answers', None)
        if with_answers and with_answers == 'False':
            return ShortQuestionSerializer
        return FullQuestionSerializer

    def get_queryset(self):
        with_answers = self.request.query_params.get('with_answers', None)
        if with_answers and with_answers == 'False':
            return QuestionModel.objects.prefetch_related('categories').all()
        return QuestionModel.objects.prefetch_related('categories', 'answers').all()


class QuestionRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = QuestionModel.objects.prefetch_related('answers').all()
    serializer_class = FullQuestionSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'id'


class CategoryListCreateView(ListCreateAPIView):
    queryset = CategoryModel.objects.all()
    permission_classes = [IsAdmin]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CategoryListSerializer
        return CategoryCreateSerializer


class CategoryRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = CategoryModel.objects.all()
    serializer_class = CategoryListSerializer
    lookup_field = 'id'
