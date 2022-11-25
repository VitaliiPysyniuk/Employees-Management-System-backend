from rest_framework.serializers import ModelSerializer
from django.db import transaction

from .models import QuizModel, QuizResultModel, QuestionModel, AnswerModel, CategoryModel


class QuizResultSerializer(ModelSerializer):
    class Meta:
        model = QuizResultModel
        fields = '__all__'


class CategoryListSerializer(ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = '__all__'


class CategoryCreateSerializer(ModelSerializer):
    class Meta:
        model = CategoryModel
        exclude = ['questions']
        extra_kwargs = {'id': {'read_only': False}}


class ShortCategoryCreateSerializer(ModelSerializer):
    class Meta:
        model = CategoryModel
        exclude = ['questions']
        read_only_fields = ['category_name', 'description']
        extra_kwargs = {'id': {'read_only': False}}


class AnswerSerializer(ModelSerializer):
    class Meta:
        model = AnswerModel
        fields = ['id', 'answer_text', 'is_correct']
        extra_kwargs = {'id': {'read_only': False, 'required': False}}


class FullQuestionSerializer(ModelSerializer):
    categories = ShortCategoryCreateSerializer(many=True, required=False)
    answers = AnswerSerializer(many=True, required=False)

    class Meta:
        model = QuestionModel
        fields = '__all__'

    def create(self, validated_data):
        answers = validated_data.pop('answers', [])
        categories = validated_data.pop('categories', [])

        categories_ids = [category.get('id') for category in categories]

        with transaction.atomic():
            question = super(FullQuestionSerializer, self).create(validated_data)
            for answer in answers:
                AnswerModel.objects.create(question=question, **answer)

            if len(categories_ids) != 0:
                categories_to_add = CategoryModel.objects.filter(id__in=categories_ids)
                question.categories.set(categories_to_add)

            return question

    def update(self, instance, validated_data):
        answers = validated_data.pop('answers', [])
        categories = validated_data.pop('categories', [])

        categories_ids = [category.get('id') for category in categories]
        if len(categories_ids) != 0:
            category_instances = CategoryModel.objects.filter(id__in=categories_ids)

        answers_to_create_data = [answer for answer in answers if not answer.get('id', None)]

        answers_to_update_data, answers_to_update_data_ids = list(), list()
        for answer in answers:
            if answer.get('id', None):
                answers_to_update_data.append(answer)
                answers_to_update_data_ids.append(answer.get('id'))
        answers_to_update_data = sorted(answers_to_update_data, key=lambda item: item.get('id'))

        answers_instances_to_delete, answers_instances_to_update = list(), list()
        for answer_instance in instance.answers.all():
            if answer_instance.id not in answers_to_update_data_ids:
                answers_instances_to_delete.append(answer_instance)
            else:
                answers_instances_to_update.append(answer_instance)

        with transaction.atomic():
            question = super(FullQuestionSerializer, self).update(instance, validated_data)

            for index, answer_instance in enumerate(answers_instances_to_update):
                if not AnswerSerializer(answer_instance).data == answers_to_update_data[index]:
                    serializer = AnswerSerializer(answer_instance, data=answers_to_update_data[index])
                    serializer.is_valid(raise_exception=True)
                    serializer.save()

            for answer_instance in answers_instances_to_delete:
                answer_instance.delete()

            for answer_data in answers_to_create_data:
                serializer = AnswerSerializer(data=answer_data)
                serializer.is_valid(raise_exception=True)
                serializer.save(question=question)

            if len(categories_ids) != 0:
                question.categories.set(category_instances)

        return question


class ShortQuestionSerializer(ModelSerializer):
    categories = CategoryCreateSerializer(many=True, required=False)

    class Meta:
        model = QuestionModel
        fields = '__all__'


class QuizCreatQuestionSerializer(ModelSerializer):
    class Meta:
        model = QuestionModel
        fields = '__all__'
        read_only_fields = ['question_text', 'answers']
        extra_kwargs = {'id': {'read_only': False}}


class QuizSerializer(ModelSerializer):
    questions = QuizCreatQuestionSerializer(many=True, required=False)

    class Meta:
        model = QuizModel
        fields = '__all__'

    def create(self, validated_data):
        questions = validated_data.pop('questions', [])
        questions_ids = [question.get('id') for question in questions]

        if len(questions_ids) != 0:
            question_instances = QuestionModel.objects.filter(id__in=questions_ids)

        with transaction.atomic():
            quiz = super(QuizSerializer, self).create(validated_data)
            if len(questions_ids) != 0 and len(question_instances) != 0:
                quiz.questions.set(question_instances)

        return quiz

    def update(self, instance, validated_data):
        questions = validated_data.pop('questions', [])
        questions_ids = [question.get('id') for question in questions]

        if len(questions_ids) != 0:
            question_instances = QuestionModel.objects.filter(id__in=questions_ids)

        with transaction.atomic():
            quiz = super(QuizSerializer, self).update(instance, validated_data)
            if len(questions_ids) != 0:
                quiz.questions.set(question_instances)

        return quiz


class ShortQuizSerializer(ModelSerializer):
    class Meta:
        model = QuizModel
        fields = '__all__'


class FullQuizSerializer(ShortQuizSerializer):
    questions = FullQuestionSerializer(many=True, required=False)


class AnswerForEmployeeSerializer(ModelSerializer):
    class Meta:
        model = AnswerModel
        exclude = ['is_correct']


class QuestionForEmployeeSerializer(ModelSerializer):
    categories = ShortCategoryCreateSerializer(many=True, required=False)
    answers = AnswerForEmployeeSerializer(many=True, required=False)

    class Meta:
        model = QuestionModel
        fields = '__all__'


class QuizForEmployeeSerializer(ModelSerializer):
    questions = QuestionForEmployeeSerializer(many=True, required=False)

    class Meta:
        model = QuizModel
        fields = '__all__'
