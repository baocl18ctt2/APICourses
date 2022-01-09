
from django.db.models import fields
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import *


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    # Chỉnh sửa url image để hiển thị hình ảnh
    # Ban đầu: "http://127.0.0.1:8000/courses/21/12/nh%E1%BA%ADp_m%C3%B4n_mmt.jpg",
    image = SerializerMethodField()

    def get_image(self, course):
        # Lấy request ra
        url_request = self.context['request']
        name = course.image.name
        if name.startswith('static/'):
            path = f'/{name}'
        else:
            path = f'/static/{name}'
        return url_request.build_absolute_uri(path)

    class Meta:
        model = Course
        fields = ['id', 'subject', 'image', 'create_date', 'category','description']


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'subject', 'image',
                  'create_date', 'update_date', 'course']


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class LessonDetailSerializer(LessonSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Lesson
        fields = LessonSerializer.Meta.fields + ['content', 'tags']


class UserSerializer(ModelSerializer):

    # overwritedding lại phương thức create để băm mật khẩu
    def create(self, validated_data):
        user = User(**validated_data)
        # Phương thức để băm mật khẩu có sẵn
        user.set_password(user.password)
        user.save()
        return user

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

    avatar = serializers.ImageField(use_url = True, required = False)
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name',
                  'username', 'password', 'email', 'date_joined', 'avatar']
        extra_kwargs = {
            'password': {'write_only': 'true'}
        }


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_date', 'updated_date']
