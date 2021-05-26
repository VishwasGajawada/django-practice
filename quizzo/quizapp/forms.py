from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import fields
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError
from .models import MyUser, Student, Teacher, Subject, Quiz, Answer


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ("username", "email", "password1", "password2", "profile_pic")


class StudentCreationForm(forms.ModelForm):
    subjects = forms.ModelMultipleChoiceField(
        label="Subjects",
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Student
        fields = ["subjects", "registration_number", "roll_no"]
        help_texts = {"subjects": "Select subjects you are enrolled or interested in"}


class TeacherCreationForm(forms.ModelForm):
    subjects = forms.ModelMultipleChoiceField(
        label="Subjects",
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Teacher
        fields = ["subjects"]
        help_texts = {"subjects": "Select subjects you assigned to"}


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ["name", "color"]


class StudentSubjectUpdateForm(forms.ModelForm):
    subjects = forms.ModelMultipleChoiceField(
        label="Subjects",
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Student
        fields = [
            "subjects",
        ]


class TeacherSubjectUpdateForm(forms.ModelForm):
    subjects = forms.ModelMultipleChoiceField(
        label="Subjects",
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Teacher

        fields = [
            "subjects",
        ]


class MyUserUpdateForm(forms.ModelForm):
    # readonly = ('username',)
    # def __init__(self, *arg, **kwrg):
    #     super(MyUserUpdateForm, self).__init__(*arg, **kwrg)
    #     for x in self.readonly:
    #         # self.fields[x].widget.attrs['disabled'] = 'disabled'
    #         self.fields[x].widget.attrs['readonly'] = True

    # def clean(self):
    #     data = super(MyUserUpdateForm, self).clean()
    #     for x in self.readonly:
    #         data[x] = getattr(self.instance, x)
    #     return data

    class Meta:
        model = MyUser
        fields = ["email", "profile_pic"]


class StudentUpdateForm(forms.ModelForm):
    # readonly = ('registration_number',)
    subjects = forms.ModelMultipleChoiceField(
        label="Subjects",
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    # def __init__(self, *arg, **kwrg):
    #     super(StudentUpdateForm, self).__init__(*arg, **kwrg)
    #     for x in self.readonly:
    #         # self.fields[x].widget.attrs['disabled'] = 'disabled'
    #         self.fields[x].widget.attrs['readonly'] = True

    # def clean(self):
    #     data = super(StudentUpdateForm, self).clean()
    #     for x in self.readonly:
    #         data[x] = getattr(self.instance, x)
    #     return data

    class Meta:
        model = Student
        fields = ["roll_no", "subjects"]


class TeacherUpdateForm(forms.ModelForm):
    subjects = forms.ModelMultipleChoiceField(
        label="Subjects",
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Teacher
        fields = ["subjects"]


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ["title", "description", "question_file"]


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ["answer_file",]
