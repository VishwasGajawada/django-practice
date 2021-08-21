from django.shortcuts import render
from .models import Blog, Comment

# Create your views here.
def index(request):
    blogs = Blog.objects.all()
    context = {'blogs' : blogs}
    return render(request, 'blog_app/index.html',context=context)

def blog_detail(request, pk):
    blog = Blog.objects.get(id=pk)
    comments = Comment.objects.filter(post = blog).order_by('path_id')

    context={'blog': blog, 'comments': comments}
    return render(request, 'blog_app/blog_detail.html',context=context)
