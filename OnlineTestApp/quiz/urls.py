from django.urls import path, re_path
from .api import QuizListAPI,QuizDetailAPI, MyQuizListAPI, SaveUsersAnswer


urlpatterns = [
	path("quizzes/", QuizListAPI.as_view()),
	re_path(r"quizzes/(?P<slug>[\w\-]+)/$", QuizDetailAPI.as_view()),
	path("my-quizzes/", MyQuizListAPI.as_view()),
	path("save-answer/", SaveUsersAnswer.as_view()),

]