from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class QuizModel(models.Model):
    class Meta:
        db_table = 'quizzes'

    title = models.CharField(max_length=60)
    description = models.CharField(max_length=200)
    is_active = models.BooleanField(default=False)
    time_constraint_in_seconds = models.IntegerField()

    creator = models.ForeignKey(UserModel, on_delete=models.PROTECT, related_name='created_quizzes')


class QuizResultModel(models.Model):
    class Meta:
        db_table = 'quizzes_results'

    max_score = models.IntegerField()
    employee_score = models.IntegerField()
    used_time_in_seconds = models.IntegerField()
    finished_at = models.DateTimeField(auto_now_add=True)

    employee = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='passed_quizzes')
    quiz = models.ForeignKey(QuizModel, on_delete=models.CASCADE, related_name='quiz_results')


class QuestionModel(models.Model):
    class Meta:
        db_table = 'questions'

    question_text = models.CharField(max_length=200)

    quizzes = models.ManyToManyField(QuizModel, related_name='questions')


class AnswerModel(models.Model):
    class Meta:
        db_table = 'answers'

    answer_text = models.CharField(max_length=60)
    is_correct = models.BooleanField(default=False)

    question = models.ForeignKey(QuestionModel, on_delete=models.CASCADE, related_name='answers')


class CategoryModel(models.Model):
    class Meta:
        db_table = 'categories'

    category_name = models.CharField(max_length=20)
    description = models.CharField(max_length=200)

    questions = models.ManyToManyField(QuestionModel, related_name='categories')


