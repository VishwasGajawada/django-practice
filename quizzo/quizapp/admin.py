from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from quizapp.models import (MyUser,Student,Teacher,Subject,Quiz,Answer)
# Register your models here.
admin.site.register(MyUser)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(Quiz)
admin.site.register(Answer)