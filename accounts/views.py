from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login


# Create your views here.
def login(request):
    if request.method == 'POST':
        # Getting the user details from form
        username = request.POST['name']
        password = request.POST['password']
        # Authenticating the user
        user = authenticate(username=username,password=password)
        # Logging in the user
        if user is not None:
            auth_login(request, user)
            return redirect('myapp:index')
        else:
            messages.error(request, "Invalid Credentials!")
            return redirect('accounts:login')
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        # Getting the information about the user from our form
        username = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        # Checking if user already exist or not
        if User.objects.filter(username=username):
            messages.warning(request, "User already exists, please log in!")
            return redirect('accounts:login')
        # Saving the user to database
        myuser = User.objects.create_user(username, email, password)
        myuser.save()
        # Redirecting to login page
        return redirect('accounts:login')
    
    return render(request, 'register.html')


def logout_user(request):
    # Logging out the user
    logout(request)
    return redirect('myapp:index')
