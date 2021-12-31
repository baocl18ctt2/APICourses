from django.db.models import query
from django.shortcuts import render
from rest_framework import status, viewsets, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from .models import *
from .serializers import CategorySerializer, CourseSerializer, LessonSerializer, LessonDetailSerializer, UserSerializer
from .paginator import BasePagination
from django.http import Http404


class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CoursesViewSet(viewsets.ViewSet, generics.ListAPIView):
    # queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = BasePagination

    # ghi đè queryset
    def get_queryset(self):
        courses = Course.objects.filter(active=True)

        # Lấy ra các tham số khi client truyền request
        q = self.request.query_params.get('q')
        # Tham số q: tìm khóa học có chứa từ q trong subjects
        if q is not None:
            courses = courses.filter(subject__icontains=q)

        # Lấy ra id của category
        cate_id = self.request.query_params.get('category_id')
        # Tham số category_id: tìm kiếm khóa học với category_id tương ứng
        if cate_id is not None:
            courses = courses.filter(category_id=cate_id)

        return courses

    # tạo ra url mới mà có liên quan đến khóa học.
    # Tìm những tiết học (lesson) liên quan đến khóa học có pk.
    # url: /courses/{course_id}/lessons
    @action(methods=['get'], detail=True, url_path='lessons')
    def get_lesson(self, request, pk):
        # Lấy khóa học course_id
        course = Course.objects.get(pk=pk)
        # Tìm kiếm những lesson có khóa học tương ứng
        lessons = course.lesson.filter(active=True)

        # Tìm kiếm theo url:
        # render dữ liệu ra api: /lessons/?q=..
        q = self.request.query_params.get('q')
        if q is not None:
            lessons = lessons.filter(subject__icontains=q)

        return Response(LessonSerializer(lessons, many=True).data,
                        status=status.HTTP_200_OK)

# Tạo url: /lessons/{lesson_id}
# Vì lấy ra lesson_id thì kế thừa từ generics.RetrieveAPIView


class LessonViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Lesson.objects.filter(active=True)
    serializer_class = LessonDetailSerializer

    # Tạo url: /lessons/{lesson_id}/tag
    @action(methods=['post'], detail=True, url_path="tags")
    def add_tag(self, request, pk):
        try:
            lesson = Lesson.objects.get(pk=pk)
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            # Lấy phần body client nhập vào
            body_tags = request.data.get("tags")
            if body_tags is not None:
                for tag in body_tags:
                    t, _ = Tag.objects.get_or_create(name=tag)
                    lesson.tags.add(t)

            lesson.save()
            return Response(self.serializer_class(lesson).data,
                            status=status.HTTP_201_CREATED)

# Tạo url: /users
# Dùng phương thức kế thừa generics.CreateAPIView để "post" methods


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
