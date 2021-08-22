from django.shortcuts import render, redirect
from .models import Blog, Comment
from .forms import BlogForm, CommentForm

# Create your views here.
def index(request):
    blogs = Blog.objects.all()
    context = {'blogs' : blogs}
    return render(request, 'blog_app/index.html',context=context)

def add_blog(request):
    form = BlogForm()

    if request.method == 'POST':
        form  = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save()
            return redirect('/')

    context = {'form' : form}
    return render(request, 'blog_app/add_blog.html', context=context)

def blog_detail(request, pk):
    blog = Blog.objects.get(id=pk)
    comments = Comment.objects.filter(post = blog).order_by('path_id')
    comment_form = CommentForm()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = blog
            comment.save()
            return redirect('blog_detail',pk=pk)

    context={'blog': blog, 'comments': comments, 'comment_form':comment_form}
    return render(request, 'blog_app/blog_detail.html',context=context)

def add_reply(request,pid,cid):
    blog = Blog.objects.get(id = pid)
    parent_comment = Comment.objects.get(id = cid)

    reply_form = CommentForm()

    if request.method == 'POST':
        reply_form = CommentForm(request.POST)
        if reply_form.is_valid():
            reply = reply_form.save(commit=False)
            reply.post = blog
            reply.parent_comment = parent_comment
            reply.save()
            return redirect('blog_detail',pk=pid)

    context = {'parent_comment': parent_comment,'reply_form':reply_form, 'blog':blog}
    return render(request, 'blog_app/add_reply.html',context=context)

def edit_blog(request, pk):
    blog = Blog.objects.get(id=pk)
    form = BlogForm(instance=blog)

    if request.method == 'POST':
        form = BlogForm(request.POST,instance=blog)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form,'blog':blog}
    return render(request, 'blog_app/edit_blog.html', context=context)

        