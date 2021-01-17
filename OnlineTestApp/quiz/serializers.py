from rest_framework import serializers
from .models import Quiz, QuizTaker, Question, Answer, UserAnswer


class QuizListSerializer(serializers.ModelSerializer):
	questions_count = serializers.SerializerMethodField()
	class Meta:
		model = Quiz
		fields = ['id', 'name', 'description', 'image', 'slug','questions_count']
		read_only_fields = ['questions_count']

	def get_questions_count(self, obj):
		return obj.question_set.all().count()

# Actual Answers
class AnswerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Answer
		fields = ['id','question','label']


class QuestionSerializer(serializers.ModelSerializer):
	answer_set =  AnswerSerializer(many=True)

	class Meta:
		model = Question
		fields = '__all__'


class UsersAnswerSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserAnswer
		fields = '__all__'


class QuizTakerSerializer(serializers.ModelSerializer):
	users_answer_set = UsersAnswerSerializer(many=True)

	class Meta:
		model = QuizTaker
		fields = '__all__'


class QuizDetailSerializer(serializers.ModelSerializer):
	quiztakers_set = serializers.SerializerMethodField()
	question_set = QuestionSerializer(many=True)

	class Meta:
		model = Quiz
		fields = '__all__'

	def get_quiztakers_set(self, obj):
		try:
			quiz_taker = QuizTaker.objects.get(user=self.contaxt['request'].user, quiz=obj)
			serializer = QuizTakerSerializer(quiz_taker)
			return serializer.data
		except QuizTaker.DoesNotExist:
			return None

