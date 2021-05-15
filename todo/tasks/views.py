from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Task
from .forms import TaskForm

# Create your views here.
def index(request):
    tasks = Task.objects.all()

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
            form.save()
            return redirect('/')

    context = {"tasks":tasks,"form":form,"oldforms":oldforms}
    return render(request,'tasks/list.html',context)

# submission of form from edit option
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
def saveChanges(request,pk):
    task = Task.objects.get(id = pk)
    if request.method == 'POST':
        form = TaskForm(request.POST,instance=task)
        if form.is_valid():
            form.save()
            return redirect('/')

    
def deleteTask(request,pk):
    task = Task.objects.get(id=pk)

    if request.method == 'POST':
        task.delete()
        return redirect('/')

    context = {'task':task}
    return render(request,'tasks/delete.html',context)