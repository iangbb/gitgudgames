from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from reviews.models import Game, Review, User, UserProfile
from reviews.forms import UserForm, UserProfileForm
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


def index(request):
    context_dict = {'heading': "Gitgud Games"}
    # Add top 5 games
    games = Game.objects.order_by('-average_rating')[:5]
    context_dict['games'] = games
    return render(request, 'reviews/index.html', context=context_dict)


def about(request):
    context_dict = {'heading': "About Us"}
    return render(request, 'reviews/about.html', context=context_dict)


def games(request):
    platforms = [platform[1] for platform in Game.PLATFORM]
    genres = [genre[1] for genre in Game.GENRE]
    context_dict = {'heading': "Games", 'genres': genres, 'platforms': platforms}
    return render(request, 'reviews/games.html', context=context_dict)


def game(request, game_slug):
    context_dict = {}
    try:
        game = Game.objects.get(slug=game_slug)
        # Filter only reviews relevent to this game
        reviews = Review.objects.filter(game=game)
        context_dict['game'] = game
        context_dict['reviews'] = reviews
    except Game.DoesNotExist:
        context_dict['game'] = None

    return render(request, 'reviews/game.html', context=context_dict)


def add_review(request, game_slug):
    context_dict = {'heading': "Add Review"}
    return render(request, 'reviews/review.html', context=context_dict)


def profile(request, user):
    context_dict = {}
    try:
        profile = UserProfile.objects.get(user=user)
        context_dict['heading'] = user.username
    except profile.DoesNotExist:
        context_dict['heading'] = "Error"

    return render(request, 'reviews/profile.html', context=context_dict)


def edit_profile(request, user):
    context_dict = {'heading': "Edit Profile"}
    context_dict['profile'] = UserProfile.objects.get(user=user)
    return render(request, 'reviews/edit.html', context=context_dict)


def register(request):
    registered = False

    if request.user.is_authenticated():
        messages.warning(request, "You can't register when you're logged in")
        return HttpResponseRedirect(reverse('index'))

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_image' in request.FILES:
                profile.profile_image = request.FILES['profile_image']

            profile.save()
            messages.success(request, "Your account has been created")
            return HttpResponseRedirect(reverse('login'))

        else:
            # TODO: proper handling of form errors
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    context_dict = {'heading': "Register", 'user_form': user_form,
                    'profile_form': profile_form, 'registered': registered}
    return render(request, 'reviews/register.html', context=context_dict)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                messages.success(request, "Logged in successfully")
                return HttpResponseRedirect(reverse('index'))
            else:
                messages.error(request, "Your account has been disabled")
                return HttpResponseRedirect(reverse('login'))

        else:
            messages.error(request, "Incorrect login details")
            return HttpResponseRedirect(reverse('login'))

    context_dict = {'heading': "Login"}
    return render(request, 'reviews/login.html', context=context_dict)


def restricted(request, status=403, message="You are not allowed to access this page"):
    context_dict = {
        'heading': "Restricted",
        'message': message,
    }
    return render(request, 'reviews/restricted.html', context=context_dict, status=status)


def user_logout(request):
    logout(request)
    messages.success(request, "You have logged out")
    return HttpResponseRedirect(reverse('index'))
