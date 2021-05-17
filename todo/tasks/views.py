from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Task
from .forms import TaskForm
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate, login as loginUser ,logout as logoutUser
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def index(request):
    user = request.user
    tasks = Task.objects.filter(user = user)
    # tasks = Task.objects.all()

    oldforms = []
    for task in tasks:
        oldform = TaskForm(instance=task)
        oldform.fields["task_id"].initial =task.id
        oldforms.append(oldform)
 
    form = TaskForm()
    #submission of new form
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = user
            task.save()
            return redirect('/')

    context = {"tasks":tasks,"form":form,"oldforms":oldforms}
    return render(request,'tasks/list.html',context)

def login(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            # print(user)
            if user is not None:
                loginUser(request, user)
                return redirect('/')
            


    context = {"form":form}
    return render(request,'tasks/login.html',context)

def signup(request):
    form = UserCreationForm()

    if request.method == 'POST':
        print(request.POST)
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                return redirect('login')
    context = {"form":form}
    return render(request,'tasks/signup.html',context)

@login_required(login_url='login')
def logout(request):
    logoutUser(request)
    return redirect('login')

# submission of form from edit option
@login_required(login_url='login')
def updateTask(request,pk):
    task = Task.objects.get(id = pk)
    form = TaskForm(instance=task)
    if request.method == 'POST':
        form = TaskForm(request.POST,instance=task)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form}
    return render(request,'tasks/update_task.html',context)

# submission of form from savechanges directly
@login_required(login_url='login')
def saveChanges(request,pk):
    task = Task.objects.get(id = pk)
    if request.method == 'POST':
        form = TaskForm(request.POST,instance=task)
        if form.is_valid():
            form.save()
            return redirect('/')

@login_required(login_url='login')
def deleteTask(request,pk):
    task = Task.objects.get(id=pk)

    if request.method == 'POST':
        task.delete()
        return redirect('/')

    context = {'task':task}
    return render(request,'tasks/delete.html',context)