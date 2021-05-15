from .models import Task
from django import forms
from django.forms import ModelForm


class TaskForm(forms.ModelForm):
    task_id  = forms.IntegerField(initial=0,required=False,widget=forms.HiddenInput())
    class Meta:
        model = Task
        fields = '__all__'