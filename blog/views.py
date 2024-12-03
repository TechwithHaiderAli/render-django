from django.shortcuts import render,redirect
from blog.models import Post, Comment,Category
from blog.forms import CommentForm
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, LoginForm
from django.contrib.auth.decorators import login_required  # Import login_required decorator
from .forms import PostForm
# Create your views here.

def blog_index(request):
    posts=Post.objects.all().order_by('-created_on')
    context={
        "posts":posts,
    }
    return render(request,"blog/index.html",context)
def blog_category(request,category):
    posts=Post.objects.filter(
        categories__name__contains=category
    ).order_by("-created_on")
    context={

        "category":category,
        "posts":posts,

    }
    return render(request,"blog/category.html",context)
def blog_detail(request,pk):
    post=Post.objects.get(pk=pk)
    
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                post=post,
            )
            comment.save()
            return HttpResponseRedirect(request.path_info)
    comments=Comment.objects.filter(post=post)
    context={
        "post":post,
        "comments":comments,
        "form":CommentForm()
    }
    return render(request,"blog/detail.html",context)
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in after registration
            return redirect('blog_index')  # Redirect to the homepage or dashboard
    else:
        form = RegisterForm()
    return render(request, 'blog/register.html', {'form': form})

# Login view
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('blog_index')  # Redirect to the homepage or dashboard
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'blog/login.html', {'form': form})

@login_required  # Ensure only logged-in users can create posts
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            # Process the categories input
            category_names = form.cleaned_data['categories'].split(',')
            categories = []
            for name in category_names:
                name = name.strip()
                category, created = Category.objects.get_or_create(name=name)
                categories.append(category)
            post.save()
            post.categories.set(categories)
            return redirect('blog_index')
    else:
        form = PostForm()

    return render(request, 'blog/create_post.html', {'form': form})