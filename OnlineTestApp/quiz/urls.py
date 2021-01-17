from django.urls import path, re_path
from .api import QuizListAPI,QuizDetailAPI


urlpatterns = [
	path("quizzes/", QuizListAPI.as_view()),
	re_path(r"quizzes/(?P<slug>[\w\-]+)/$", QuizDetailAPI.as_view()),
]