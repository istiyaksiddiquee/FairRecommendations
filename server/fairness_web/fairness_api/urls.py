from django.urls import path, re_path
from fairness_api import views

urlpatterns = [
    path('researchInterests/', views.ResearchInterest.as_view()),
    re_path(r'recommendation/', views.Recommendation.as_view()),
    re_path(r'users/', views.User.as_view()),
]