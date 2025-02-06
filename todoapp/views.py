from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request, 'todoapp/home.html')

def user_login(request):
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