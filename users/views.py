from django.shortcuts import render, redirect
from .models import app_user_mst
from django.contrib import messages
from django.contrib.auth import login


def SignUp(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        f_name = request.POST.get('f_name')
        l_name = request.POST.get('l_name')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirm-password')

        if not user_name or not f_name or not l_name or not mobile or not email or not password:
            messages.error(
                request, 'Check all the data correctly don\'t enter empty values')
            return redirect('signup')

        if password != confirmPassword:
            messages.error(request, 'Password mismatch')
            return redirect('signup')

        if app_user_mst.objects.filter(user_name=user_name).exists():
            messages.error(request, 'Username is already taken')
            return redirect('signin')

        newuser = app_user_mst(user_name=user_name, f_name=f_name,
                               l_name=l_name, password=password, mobile=mobile, email=email)
        newuser.save()
        messages.success(request, 'User created successfully')
        return redirect('signin')
    else:
        return render(request, 'users/signup.html')


def SignIn(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')

        if not user_name or not password:
            messages.error(request, 'missing or Invalid username or password')
            return redirect('signin')

        registered_user = app_user_mst.objects.get(user_name=user_name)

        if registered_user:
            messages.success(request, 'User Login Successfully')
            return redirect('home-page')
        else:
            messages.error(request, 'User is not registered.')
            return redirect('signup')
    return render(request, 'users/signin.html')


# this page is only visible when webisite is opened
def Home(request):
    return render(request, 'users/home.html')


# after user login this page will be showned
def HomePage(request):
    return render(request, 'users/home_page.html')
