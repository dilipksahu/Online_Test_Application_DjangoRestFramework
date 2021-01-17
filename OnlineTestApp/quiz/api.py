from django.shortcuts import render, get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db.models import Q
from quiz.models import Quiz, QuizTaker, Question, Answer, UserAnswer
from quiz.serializers import QuizListSerializer, QuizDetailSerializer,MyQuizListSerializer, UsersAnswerSerializer


class MyQuizListAPI(generics.ListAPIView):
	permission_classes = [
		permissions.IsAuthenticated
	]
	serializer_class = MyQuizListSerializer

	def get_queryset(self, *args, **kwargs):
		queryset = Quiz.objects.filter(quiztaker__user=self.request.user)
		query = self.request.GET.get("q")

		# /api/quizzes/?q= question
		if query:
			queryset = queryset.filter(
				Q(name__icontains=query) |
				Q(description_icontains=query)

			).distinct()
		return queryset


class QuizListAPI(generics.ListAPIView):
	serializer_class = QuizListSerializer
	permission_classes = [
		permissions.IsAuthenticated
	]

	def get_queryset(self, *args, **kwargs):
		# queryset = Quiz.objects.filter(roll_out=True)
		# show all quizzes not specific to any user
		queryset = Quiz.objects.filter(roll_out=True).exclude(quiztaker__user=self.request.user)
		query = self.request.GET.get("q")

		if query:
			queryset = queryset.filter(
				Q(name__icontains=query) |
				Q(description_icontains=query)

			).distinct()

		return queryset


class QuizDetailAPI(generics.RetrieveAPIView):
	serializer_class = QuizDetailSerializer
	permission_classes = [
		permissions.IsAuthenticated
	]

	def get(self, *args, **kwargs):
		slug = self.kwargs["slug"]
		quiz = get_object_or_404(Quiz, slug=slug)
		last_question = None
		obj, created = QuizTaker.objects.get_or_create(user=self.request.user, quiz=quiz)
		if created:
			for question in Quiz.objects.filter(quiz=quiz):
				UserAnswer.objects.create(quiz_taker=obj, question=question)
		else:
			last_question = UserAnswer.objects.filter(quiz_taker=obj, answer__isnull=False)
			if last_question.count() > 0:
				last_question = last_question.last().question.id
			else:
				last_question = None

		return Response({
			'quiz': self.get_serializer(quiz, context={'request': self.request}).data,
			'last_question_id': last_question
		})


class SaveUsersAnswer(generics.UpdateAPIView):
	serializer_class = UsersAnswerSerializer
	permission_classes = [
		permissions.IsAuthenticated
	]

	def patch(self, request, *args, **kwargs):
		quiztaker_id = request.data['quiztaker']
		question_id = request.data['question']
		answer_id = request.data['answer']

		quiztaker = get_object_or_404(QuizTaker, id=quiztaker_id)
		question = get_object_or_404(Question, id=question_id)
		answer = get_object_or_404(Answer, id=answer_id)

		if quiztaker.completed:
			return Response({
				"message": "This quiz is already complete. you can't answer any more questions"},
				status=status.HTTP_412_PRECONDITION_FAILED
			)

		obj = get_object_or_404(UserAnswer, quiz_taker=quiztaker, question=question)
		obj.answer = answer
		obj.save()

		return Response(self.get_serializer(obj).data)