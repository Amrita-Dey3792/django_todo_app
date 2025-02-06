from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

@login_required
def home(request):

    return render(request, 'todoapp/home.html')

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
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        conf_password = request.POST['confPassword']

        if password != conf_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('user_register')
        
        if len(password) < 6 or len(conf_password) < 6:
            messages.error(request, 'Password should be at least 6 characters long.')
            return redirect('user_register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('user_register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('user_register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, 'Registration successful. You can now log in.')
        return redirect('user_login')

    return render(request, 'todoapp/signup.html')


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('user_login')

