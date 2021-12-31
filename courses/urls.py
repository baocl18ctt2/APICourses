from rest_framework import routers
from . import views
from django.urls import path, include
# Create your views here.

# Khởi tạo routers
router = routers.DefaultRouter()
router.register('categories', views.CategoryViewSet, 'category')
router.register('courses', views.CoursesViewSet, 'course')
router.register('lessons', views.LessonViewSet, 'lesson')
router.register('users', views.UserViewSet, 'user')

urlpatterns = [
    path('', include(router.urls)),
]
