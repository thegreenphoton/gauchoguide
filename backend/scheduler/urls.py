from django.urls import path
from .views import CourseSchedulerView, ElectivesView, CareerRecommendationView

urlpatterns = [
    path('electives/', ElectivesView.as_view(), name='electives'),
    path('career-results/', CareerRecommendationView.as_view(), name='career-results'),
    path('schedule-builder/', CourseSchedulerView.as_view(), name='schedule-builder'),
]
