from django.template.defaultfilters import slugify
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django import forms

from .forms import (
    StudentCreationForm,
    MyUserCreationForm,
    TeacherCreationForm,
    SubjectForm,
    StudentSubjectUpdateForm,
    TeacherSubjectUpdateForm,
    MyUserUpdateForm,
    StudentUpdateForm,
    TeacherUpdateForm,
    QuizForm,
    AnswerForm,
)
from .models import MyUser, Student, Teacher, Subject, Quiz, Answer

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import CreateView
from django.db.models import Avg
from django.db.models.functions import Coalesce

# Create your views here.


def getSubjects(user):
    if user.is_student:
        return user.student.subjects.all()
    if user.is_teacher:
        return user.teacher.subjects.all()


@login_required(login_url="login")
def index(request):
    subjects = []
    user = request.user
    if user.is_authenticated:
        subjects = getSubjects(user)
    context = {"subjects": subjects}
    return render(request, "quizapp/index.html", context)


def signup(request):
    return render(request, "registration/signup.html")


def student_signup(request):
    user_form = MyUserCreationForm()
    student_form = StudentCreationForm()
    context = {"user_form": user_form, "student_form": student_form}
    if request.method == "POST":
        user_form = MyUserCreationForm(request.POST, request.FILES)
        student_form = StudentCreationForm(request.POST)
        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save(commit=False)
            user.is_student = True
            user.save()
            student = student_form.save(commit=False)
            student.user = user
            student.save()
            student_form.save_m2m()  # for saving subjects..since it requires separate tavble
            return redirect("login")

    return render(request, "registration/student_signup.html", context)


def teacher_signup(request):
    user_form = MyUserCreationForm()
    teacher_form = TeacherCreationForm()
    context = {"user_form": user_form, "teacher_form": teacher_form}
    if request.method == "POST":
        user_form = MyUserCreationForm(request.POST, request.FILES)
        teacher_form = TeacherCreationForm(request.POST)
        if user_form.is_valid() and teacher_form.is_valid():
            user = user_form.save(commit=False)
            user.is_teacher = True
            user.save()
            teacher = teacher_form.save(commit=False)
            teacher.user = user
            teacher.save()
            teacher_form.save_m2m()
            return redirect("login")

    return render(request, "registration/teacher_signup.html", context)


# @login_required(login_url='login')
class SubjectCreateView(LoginRequiredMixin, CreateView):
    model = Subject
    fields = ["name", "color"]
    template_name = "quizapp/subject_add.html"
    login_url = "login"
    redirect_to = "index"


@login_required(login_url="login")
def create_subject(request):
    if request.user.is_student:
        return redirect("index")

    subjects = request.user.teacher.subjects.all()
    form = SubjectForm()
    if request.method == "POST":
        form = SubjectForm(request.POST)
        sub = request.POST.get("name")
        slug = slugify(sub)
        if Subject.objects.filter(slug=slug).exists():
            print("already exists")
            messages.error(request, "Subject already exists")
            context = {"form": form, "subjects": subjects}
            return render(request, "quizapp/subject_create.html", context)

        if form.is_valid():
            form.save()
            return redirect("index")

    context = {"form": form, "subjects": subjects}
    return render(request, "quizapp/subject_create.html", context)


@login_required(login_url="login")
def add_subject(request):
    user = request.user
    subjects = getSubjects(user)
    if user.is_student:
        profile = user.student
        form = StudentSubjectUpdateForm(instance=profile)
    else:
        profile = user.teacher
        form = TeacherSubjectUpdateForm(instance=profile)

    if request.method == "POST":
        if user.is_student:
            form = StudentSubjectUpdateForm(request.POST, instance=profile)
        else:
            form = TeacherSubjectUpdateForm(request.POST, instance=profile)

        if form.is_valid():
            form.save(commit=False)
            form.save_m2m()
            return redirect("index")

    context = {"subjects": subjects, "form": form}
    return render(request, "quizapp/subject_add.html", context)


@login_required(login_url="login")
def show_subject(request, subject_slug):
    user = request.user
    quizform = None
    subject = Subject.objects.get(slug=subject_slug)
    quizzes = Quiz.objects.filter(subject=subject).order_by("-created_time")
    subjects = getSubjects(user)
    
    if user.is_teacher:
        quizform = QuizForm()

    if subject not in subjects:
        return redirect("index")
    # adding a new quiz
    if request.method == "POST" and user.is_teacher:
        quizform = QuizForm(request.POST, request.FILES)
        if quizform.is_valid():
            question_description = request.POST.get("description")
            # print(question_description)
            if "question_file" not in request.FILES and not len(question_description):
                print("mistake")
                messages.error(request, "Atlest provide either description or file")
                context = {
                    "subject": subject,
                    "subjects": subjects,
                    "quizzes": quizzes,
                    "quizform": quizform,
                }
                return render(request, "quizapp/subject.html", context)
            quiz = quizform.save(commit=False)
            quiz.subject = subject
            quiz.teacher = user.teacher
            quiz.save()
            return HttpResponseRedirect(
                reverse("subject", kwargs={"subject_slug": subject_slug})
            )

    context = {
        "subject": subject,
        "subjects": subjects,
        "quizzes": quizzes,
        "quizform": quizform,
    }
    return render(request, "quizapp/subject.html", context)


@login_required(login_url="login")
def subject_people(request, subject_slug):
    user = request.user
    subject = Subject.objects.get(slug=subject_slug)
    teachers = Teacher.objects.filter(subjects=subject)
    students = Student.objects.filter(subjects=subject)
    subjects = getSubjects(user)

    context = {
        "teachers": teachers,
        "students": students,
        "subjects": subjects,
        "subject": subject,
    }
    return render(request, "quizapp/subject_people.html", context)


@login_required(login_url="login")
def subject_grades(request, subject_slug):
    user = request.user
    subject = Subject.objects.get(slug=subject_slug)
    quizzes = Quiz.objects.filter(subject=subject).order_by("-created_time")
    answers = None
    subjects = getSubjects(user)
    if user.is_student:
        answers = Answer.objects.filter(
            quiz__in=quizzes, student=user.student
        ).order_by("-quiz__created_time")
        print(answers)
    context = {
        "subjects": subjects,
        "subject": subject,
        "quizzes": quizzes,
        "answers": answers,
    }
    # context = {}
    return render(request, "quizapp/subject_grades.html", context)


@login_required(login_url="login")
def profile(request):
    user = request.user
    user_form = MyUserUpdateForm(instance=user)
    subjects = getSubjects(user)
    if user.is_student:
        profile = user.student
        profile_form = StudentUpdateForm(instance=profile)
    else:
        profile = user.teacher
        profile_form = TeacherUpdateForm(instance=profile)

    if request.method == "POST":
        user_form = MyUserUpdateForm(request.POST, request.FILES, instance=user)
        if user.is_student:
            profile_form = StudentUpdateForm(request.POST, instance=profile)
        else:
            profile_form = TeacherUpdateForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save(commit=False)
            profile_form.save_m2m()
            return redirect("profile")

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
        "subjects": subjects,
        "profile": profile,
    }
    return render(request, "quizapp/profile.html", context)


@login_required(login_url="login")
def quiz_detail(request, subject_slug, pk):

    user = request.user
    subject = Subject.objects.get(slug=subject_slug)
    quiz = Quiz.objects.get(id=pk)
    subjects = getSubjects(user)
    # quiz_answers = Answer.objects.filter(quiz = quiz)
    # avg_score = quiz_answers.aggregate(mark = Coalesce(Avg('score'),0.0))
    # print(avg_score)

    # for student
    answer_form = None
    answer = None
    submitted = False

    # for teacher
    submitted_answers = None

    if user.is_student:
        answer = Answer.objects.filter(quiz=quiz, student=user.student)
        if len(answer) > 0:
            answer = answer[0]
            print(answer)
            submitted = True
        answer_form = AnswerForm()
    else:
        submitted_answers = Answer.objects.filter(quiz=quiz)

    if request.method == "POST" and user.is_student:
        answer_form = AnswerForm(request.POST, request.FILES)
        if answer_form.is_valid():
            answer = answer_form.save(commit=False)
            answer.student = user.student
            answer.quiz = quiz
            answer.save()
            return redirect("quiz_detail", subject_slug=subject_slug, pk=pk)

    context = {
        "subject": subject,
        "subjects": subjects,
        "quiz": quiz,
        "answer_form": answer_form,
        "answer": answer,
        "submitted": submitted,
        "submitted_answers": submitted_answers,
    }
    return render(request, "quizapp/quiz_detail.html", context)


@login_required(login_url="login")
def mark_answer(request, pk):
    user = request.user
    answer = Answer.objects.get(id=pk)
    quiz = answer.quiz
    subject = quiz.subject

    quiz_answers = Answer.objects.filter(quiz=quiz) #to update average
    if user.is_student or (
            user.is_teacher and subject not in user.teacher.subjects.all()
        ):
        return redirect("index")

    if request.method == "POST":
        score = request.POST.get("score")
        answer.score = score
        answer.save()
        
        avg_score = quiz_answers.aggregate(mark=Coalesce(Avg("score"), 0.0))["mark"]
        # print(avg_score)
        quiz.avg_score = avg_score
        quiz.save()
    return redirect("quiz_detail", subject_slug=subject.slug, pk=quiz.id)
