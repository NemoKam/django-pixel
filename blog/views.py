import re
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Post 
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import  render
from django.core.files.storage import FileSystemStorage
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})
def post_new(request):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save()
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            response = HttpResponse('blah')
            response.delete_cookie('lastpost')
            response.set_cookie('lastpost', str(timezone.now()))
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})    
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form, 'post':post})
def post_delete(request , pk):
    post_to_delete=Post.objects.get(pk=pk)
    post_to_delete.delete()
    return redirect('post_list')

def register(request):
    if request.method == "POST":
        user = User.objects.create_user(request.POST['username'],  request.POST['email'], request.POST['password'])
        user.first_name = request.POST['name']
        user.last_name = request.POST['surname']
        user.save()
        return redirect('post_list')
    return render(request, 'registration/register.html')
    
def setcookie(request):
    response = HttpResponse('blah')
    response.set_cookie('lastpost', str(timezone.now()))
    return response
def getcookie(request):
    value = request.COOKIES.get('lastpost')
    response = HttpResponse(value)
    return response
def play(request):
    return render(request, 'blog/play.html')
