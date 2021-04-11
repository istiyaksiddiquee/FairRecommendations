from django.urls import path
from fairness_api import views

urlpatterns = [
    path('hello-view/', views.HelloApiView.as_view()),
    path('test-pytable/', views.PyTableTester.as_view()),
    path('researchInterests/', views.ResearchInterest.as_view()),
]