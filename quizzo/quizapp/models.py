from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify
from PIL import Image
from .utils import *

# Create your models here.
class MyUser(AbstractUser):
    email = models.EmailField(max_length=264)
    profile_pic = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super().save()
        if self.profile_pic:
            image = Image.open(self.profile_pic.path)
            image = make_square(image)
            image.save(self.profile_pic.path)


class Subject(models.Model):
    COLOR_CHOICES = [
        ("#E06C75", "RED"),
        ("#E5C07B", "YELLOW"),
        ("#98C379", "GREEN"),
        ("#61AFEF", "BLUE"),
        ("#863A95", "PURPLE"),
    ]
    name = models.CharField(max_length=256, primary_key=True)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, default="#863A95")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Subject, self).save(*args, **kwargs)


class Student(models.Model):
    user = models.OneToOneField(
        MyUser, on_delete=models.CASCADE, related_name="student"
    )
    subjects = models.ManyToManyField(Subject, related_name="students", blank=True)
    registration_number = models.IntegerField(primary_key=True)
    roll_no = models.IntegerField()

    def __str__(self):
        return self.user.username + " " + str(self.registration_number)


class Teacher(models.Model):
    user = models.OneToOneField(
        MyUser, on_delete=models.CASCADE, related_name="teacher"
    )
    subjects = models.ManyToManyField(Subject, related_name="teachers", blank=True)

    def __str__(self):
        return self.user.username


class Quiz(models.Model):
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, related_name="quizzes"
    )
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="quizzes"
    )
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=300, blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    question_file = models.FileField(upload_to="question_files/", blank=True, null=True)
    avg_score = models.FloatField(default=None, blank=True, null=True)

    def __str__(self):
        return self.subject.name + "-" + self.title + " - " + str(self.id)


class Answer(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="answers"
    )
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="answers")
    score = models.PositiveIntegerField(blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    answer_file = models.FileField(upload_to="answer_files/")

    def __str__(self):
        return self.quiz.title + "-answer-" + str(self.id)
