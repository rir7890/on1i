from django.shortcuts import render


def SignUp(request):
    return render(request, 'users/signup.html')


def SignIn(request):
    return render(request, 'users/signin.html')


def Home(request):
    return render(request, 'users/home.html')
