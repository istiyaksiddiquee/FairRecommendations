from django.urls import path
from fairness_api import views

urlpatterns = [
    path('hello-view/', views.HelloApiView.as_view()),
    path('researchInterests/', views.ResearchInterest.as_view()),
    path('h5Demo/', views.DemoForH5.as_view()),
]