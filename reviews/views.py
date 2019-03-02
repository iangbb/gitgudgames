from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context_dict = {'heading': "Gitgud Games"}
    return render(request, 'reviews/index.html', context=context_dict)

def about(request):
    context_dict = {'heading': "About Us"}
    return render(request, 'reviews/about.html', context=context_dict)

def games(request):
    context_dict = {'heading': "Games"}
    return render(request, 'reviews/games.html', context=context_dict)

def game(request):
    context_dict = {'heading': "Gitgud Games"}
    return render(request, 'reviews/game.html', context=context_dict)

def profile(request):
    context_dict = {'heading': "Profile"}
    return render(request, 'reviews/profile.html', context=context_dict)

def edit(request):
    context_dict = {'heading': "Edit Profile"}
    return render(request, 'reviews/edit.html', context=context_dict)

def register(request):
    context_dict = {'heading': "Register"}
    return render(request, 'reviews/register.html', context=context_dict)

def login(request):
    context_dict = {'heading': "Login"}
    return render(request, 'reviews/login.html', context=context_dict)

def restricted(request):
    context_dict = {'heading': "Restricted"}
    return render(request, 'reviews/restricted.html', context=context_dict)

def review(request):
    context_dict = {'heading': "Review"}
    return render(request, 'reviews/review.html', context=context_dict)
