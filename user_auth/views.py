from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

User = get_user_model()


def register_process(request):
    """ Register User"""
    if not request.user.is_authenticated:
        if request.method == "POST":
            full_name = request.POST['name']
            email = request.POST['email']
            password = request.POST['password']

            full_name = full_name.split(" ")
            last_name = " "
            if len(full_name) > 1:
                last_name = full_name[1]
            first_name = full_name[0]

            if User.objects.filter(email=email).exists():
                return render(request, "login.html", {'mesage': 'User already exists with this email.'})

            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            login(request, user)
            return render(request, "home.html", {'mesage': 'Register successfully.'})

        return render(request, "register.html")
    return render(request, "home.html", {'mesage': 'You are already logged in.'})


def login_process(request):
    """Login user"""
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST['email']
            password = request.POST['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                # return render(request, "settings.html", {'mesage': 'Login successfully.'})
                return redirect('home')
            message = 'Invalid credentials.'
            return render(request, 'login.html', {'message': message})

        return render(request, "login.html")
    return render(request, "home.html", {'mesage': 'You are already logged in.'})

@login_required
def logout_process(request):
    """Logout user"""
    if request.user.is_authenticated:
        logout(request)
        # return render(request, 'login.html', {'message': 'Logout successfully.'})
        return redirect('login')
    return render(request, 'login.html')
