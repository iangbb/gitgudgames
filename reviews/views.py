from django.shortcuts import render
from django.http import HttpResponse
from reviews.models import Game

def index(request):
    context_dict = {'heading': "Gitgud Games"}
    return render(request, 'reviews/index.html', context=context_dict)

def about(request):
    context_dict = {'heading': "About Us"}
    return render(request, 'reviews/about.html', context=context_dict)

def games(request):
    platforms = [platform[1] for platform in Game.PLATFORM]
    genres = [genre[1] for genre in Game.GENRE]
    context_dict = {'heading': "Games", 'genres': genres, 'platforms': platforms}
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
