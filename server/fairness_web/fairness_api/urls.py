from django.urls import path, re_path
from fairness_api import views

urlpatterns = [
    path('hello-view/', views.HelloApiView.as_view()),
    path('researchInterests/', views.ResearchInterest.as_view()),
    re_path(r'h5Demo/', views.DemoForH5.as_view()),
]