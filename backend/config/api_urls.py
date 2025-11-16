from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.tests.views import LessonViewSet, TestViewSet, QuestionViewSet

router = DefaultRouter()
router.register(r'lessons', LessonViewSet, basename='lesson')
router.register(r'tests', TestViewSet, basename='test')
router.register(r'questions', QuestionViewSet, basename='question')

urlpatterns = [
    path('', include(router.urls)),
]
