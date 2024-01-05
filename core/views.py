# views.py
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login  
from django.contrib.auth import logout as auth_logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required

def index(request):
    count = User.objects.count()
    usernames = User.objects.all()
    return render(request, 'index.html')
   
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken. Please choose another.')
            return render(request, 'registration/signup.html')

        # Check if the passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'registration/signup.html')

        # Create a new user (you may want to add additional validation and error handling)
        user = User.objects.create_user(username=username, email=email, password=password, is_staff=False)

        # Log the user in
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)  # Use auth_login instead of login
            messages.success(request, 'Account created successfully. You are now logged in.')
            return redirect('home')

    return render(request, 'registration/signup.html')


def login(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')

        # Try to authenticate by both username and email
        user = authenticate(request, username=username_or_email, password=password)

        if user is None:
            # If authentication fails with username, try with email
            user = User.objects.filter(Q(username=username_or_email) | Q(email=username_or_email)).first()
            if user:
                user = authenticate(request, username=user.username, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials.')

    return render(request, 'registration/login.html')


def logout(request):
    auth_logout(request)
    return redirect('index')

   
@login_required 
def home(request):
    count = User.objects.count()
    usernames = User.objects.all()
    return render(request, 'home.html', {
        'count': count,
        'usernames': usernames,
    })