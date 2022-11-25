from rest_framework.exceptions import ParseError


def evaluate_user_answers(user_answers, correct_answers, request):
    if len(correct_answers) != len(user_answers):
        raise ParseError('Quiz result includes the wrong number of answers on quiz`s questions.')

    user_answers = sorted(user_answers, key=lambda item: item.get('question_id'))

    data = {
        'max_score': len(correct_answers),
        'employee_score': 0,
        'used_time_in_seconds': request.data.get('used_time_in_seconds'),
        'quiz': request.data.get('quiz'),
        'employee': request.user.id
    }

    for index, answer in enumerate(correct_answers):
        if answer.id == user_answers[index]['answer_id']:
            data['employee_score'] += 1

    return data
