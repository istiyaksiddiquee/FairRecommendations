from django.urls import path, re_path
from fairness_api import views

urlpatterns = [
    re_path(r'researchInterests/', views.ResearchInterest.as_view()),
    re_path(r'databaseReset/', views.DatabaseReset.as_view()),
    re_path(r'recommendation/', views.Recommendation.as_view()),
    re_path(r'initialization/', views.Initialization.as_view()),
    re_path(r'users/', views.User.as_view()),
]