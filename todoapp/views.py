from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CategoryForm, TaskForm
from .models import Category, Task, UserInfo
from django.utils import timezone
import string
import random
from django.urls import reverse
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

# Create your views here.
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials.')   
        
    return render(request, 'todoapp/login.html')


def user_register(request): 

    if request.method == 'POST':
        username = request.POST['username'].strip()
        email = request.POST['email'].strip()
        password = request.POST['password']
        conf_password = request.POST['confPassword']

        if password != conf_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('user_register')
        
        if len(password) < 6 or len(conf_password) < 6:
            messages.error(request, 'Password should be at least 6 characters long.')
            return redirect('user_register')
        
        print(User.objects.filter(username=username).exists())

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('user_register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('user_register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        UserInfo(user=user).save()
        messages.success(request, 'Registration successful. You can now log in.')
        return redirect('user_login')

    return render(request, 'todoapp/signup.html')


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('user_login')

def forgot_password(request):

    if request.method == 'POST':
        email = request.POST['email']
        user = User.objects.filter(email=email).first()

        
        if user:
            reset_code = ''.join(random.choices(string.ascii_letters + string.digits, k=200))
            user.userinfo.password_reset_code = reset_code
            user.userinfo.reset_code_created_at = timezone.now()
            user.userinfo.save()

            # Create password reset link
            'http://localhost:8000/reset_password/lm12UnAN8prqUMgzfSDFyRX4L9A4QeP8VML2HNiF2bCJ8M0yBi3uTOX85wejCQ0Qiq9Jpelof0WJGYtnKX1ePhukZORvO6guAjzYFahVR1rbJrEKfCRjaqncHU8LGrV6JHR5jvX2UCLz13bYXimxPUcNTgkr5WHSnd6C0O6MjSxVWMQ6TC43YnD85mgGHyhMiwOzYuTO'
            reset_link = request.build_absolute_uri(reverse("reset_password", kwargs={"reset_code": reset_code}))

    
            # Render the HTML template with context
            html_content = render_to_string("todoapp/reset_password_email_template.html", {"user": user, "reset_link": reset_link})
            
            # Create email
            email = EmailMessage(
                subject='Your Password Reset Link',
                body=html_content,
                from_email=settings.EMAIL_HOST_USER,
                to=[user.email],
            )
            email.content_subtype = 'html' # Set content type to HTML
            email.send(fail_silently=False)

            messages.success(request, "Password reset link sent to your email.")
            return redirect("forgot_password")
        
        else:
            messages.error(request, 'No user found with that email address.')

    return render(request, 'todoapp/forgot_password.html')


def reset_password(request, reset_code):

    try:
        userInfo = UserInfo.objects.get(password_reset_code=reset_code)

        print(userInfo.is_reset_code_expired())

        if userInfo.is_reset_code_expired():
            return HttpResponse("Reset code has expired.", status=400)
        
        if request.method == "POST":
            password = request.POST.get("password")
            confPassword = request.POST.get("confPassword")

            if password != confPassword:
                messages.error(request, "Passwords do not match")
                return redirect("reset_password", reset_code=reset_code)
                
            userInfo.user.set_password(password)
            userInfo.user.save()

            userInfo.password_reset_code = None
            userInfo.reset_code_created_at = None
            userInfo.save()

            login(request, userInfo.user)
            messages.success(request, "Your password has been changed successfully!")
            return redirect("home")


        return render(request, "todoapp/reset_password.html")

    except Exception as e:
        print(e)
        return HttpResponse("Invalid Reset Code")


@login_required
def add_category(request):
    form = CategoryForm()
    return render(request, 'todoapp/category_form.html', {'form': form})


@login_required
def home(request):
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    print(tasks)

    return render(request, 'todoapp/home.html', {'tasks': tasks})

@login_required
def add_task(request):
    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Task added successfully.')
            return redirect('home')

    return render(request, 'todoapp/create_task.html', {'form': form})


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    form = TaskForm(instance=task)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            messages.success(request, 'Task updated successfully.')
            return redirect('home')

    return render(request, 'todoapp/create_task.html', {'form': form}) 


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    messages.success(request, 'Task deleted successfully.')
    return redirect('home')


@login_required
def category_list(request):
    categories = Category.objects.filter(user=request.user)
    return render(request, 'todoapp/category_list.html', {'categories': categories})


@login_required
def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, 'Category added successfully.')
            return redirect('category_list')
    return render(request, 'todoapp/category_form.html', {'form': form})


@login_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id, user=request.user)
    form = CategoryForm(instance=category)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            messages.success(request, 'Category updated successfully.')
            return redirect('category_list')
    return render(request, 'todoapp/category_form.html', {'form': form})


@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id, user=request.user)
    category.delete()
    messages.success(request, 'Category deleted successfully.')
    return redirect('category_list')

