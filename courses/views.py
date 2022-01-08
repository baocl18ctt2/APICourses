from django.db.models import query
from django.shortcuts import render
from rest_framework import status, viewsets, generics, permissions
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from django.conf import settings
from rest_framework.views import APIView
from .models import *
from .serializers import CategorySerializer, CourseSerializer, LessonSerializer, LessonDetailSerializer, UserSerializer, CommentSerializer
from .paginator import BasePagination
from django.http import Http404

from courses import serializers


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
    # Tìm những tiết học (lesson) liên quan đến khóa học cụ thể có pk.
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


class LessonViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Lesson.objects.filter(active=True)
    serializer_class = LessonDetailSerializer

    # Kiểm tra permission để chứng thực
    def get_permissions(self):
        if self.action == 'add_comment':
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    # Tạo url: /lessons/{lesson_id}/tag
    @action(methods=['post'], detail=True, url_path="tags")
    def add_tag(self, request, pk):
        # Kiểm tra xem có tồn tại đối tượng lesson đó ko
        try:
            lesson = Lesson.objects.get(pk=pk)
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            # Lấy phần body client nhập vào
            body_tags = request.data.get("tags")
            if body_tags is not None:
                for tag in body_tags:
                    # thêm tags mới vào model Tag
                    t, _ = Tag.objects.get_or_create(name=tag)
                    # add thêm tags vào trong lessons
                    lesson.tags.add(t)
            # lưu lại lesson sau khi thêm tags
            lesson.save()
            return Response(self.serializer_class(lesson).data,
                            status=status.HTTP_201_CREATED)

    # Tạo url: lessons/{lesson_id}/comments để add thêm comment vào lessons
    @action(methods=['post'], detail=True, url_path='comments')
    def add_comment(self, request, pk):
        # Lấy request khi gửi dữ liệu add_comment
        content = request.data.get('content')
        # Nếu có nội dung comment
        if content:
            c = Comment.objects.create(content=content,
                                       lesson=Lesson.objects.get(pk=pk),
                                       creator=request.user)
            return Response(CommentSerializer(c).data, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)

# Tạo url: /users
# Dùng phương thức kế thừa generics.CreateAPIView để "post" (thêm mới) methods


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.UpdateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'get_current_user':
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    # lấy ra user hiện tại đã đăng nhập
    # Tạo url mới: /users/current-user

    @action(methods=['get'], detail=False, url_path="current-user")
    def get_current_user(self, request):
        return Response(self.serializer_class(request.user).data,
                        status=status.HTTP_200_OK)


# Tạo url: /comments/{comments_id} để xóa chi tiết 1 comment


class CommentViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentSerializer

    # Xóa chi tiết comment
    def destroy(self, request, *args, **kwargs):
        # Kiểm tra request của user hiện tại có đúng là của user đã tạo ra comment
        if request.user == self.get_object().creator:
            return super().destroy(request, *args, **kwargs)
        # Không đúng user thì cấm ko cho xóa
        return Response(status=status.HTTP_403_FORBIDDEN)

    # update content của comment
    def partial_update(self, request, *args, **kwargs):
        if request.user == self.get_object().creator:
            return super().partial_update(request, *args, **kwargs)

        return Response(status=status.HTTP_403_FORBIDDEN)


# tạo url: /oauth2_info để lấy client_id và client_secret


class AuthInfo(APIView):
    def get(self, request):
        return Response(settings.OAUTH2_INFO, status=status.HTTP_200_OK)
