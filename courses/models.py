from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields.files import ImageField
# Create your models here.


class User(AbstractUser):
    avatar = models.ImageField(upload_to='uploads/%Y/%m')


class Category(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)

    # Xuất thông tin hiển thị khi sử dụng terminal chạy model
    def __str__(self):
        return self.name


class MyModelBase(models.Model):
    class Meta:
        abstract = True

    subject = models.CharField(max_length=255, null=True)
    image = models.ImageField(upload_to='courses/%y/%m', default=None)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.subject


# Sử dụng MyModelBase để kế thừa các thuộc tính


class Course(MyModelBase):
    # Sử dụng class meta để tràng buộc
    class Meta:
        unique_together = ('subject', 'category')
        ordering = ["-id"]

    # Thêm các thuộc tính khác cho từng khóa học
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)


class Lesson(MyModelBase):
    class Meta:
        unique_together = ('subject', 'course')

    content = models.TextField()
    course = models.ForeignKey(
        Course, related_name="lesson", on_delete=models.CASCADE)
    tags = models.ManyToManyField(
        'Tag', related_name='lesson', blank=True, null=True)


class Comment(models.Model):
    content = models.TextField()
    # khi xóa lessons thì comment cũng xóa
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# Tạo model để thực hiện các tính năng like, đếm số lượt view


class ActionBase(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Action(ActionBase):
    LIKE, HAHA, HEART = range(3)
    ACTIONS = [
        (LIKE, 'like'),
        (HAHA, 'haha'),
        (HEART, 'heart')
    ]
    type = models.PositiveSmallIntegerField(choices=ACTIONS, default=LIKE)


class Rating(ActionBase):
    rate = models.PositiveSmallIntegerField(default=0)
