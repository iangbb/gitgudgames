from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from reviews.models import Game, Review, Comment, User, UserProfile, Image, Comment
from reviews.forms import UserForm, UserProfileForm, ReviewForm


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
        reviews = Review.objects.filter(game=game).order_by('-votes')
        pictures = Image.objects.filter(game=game)
        comments = Comment.objects.filter(review=reviews)
        context_dict['game'] = game
        context_dict['reviews'] = reviews
        context_dict['pictures'] = pictures
        context_dict['comments'] = comments
    except Game.DoesNotExist:
        context_dict['game'] = None

    return render(request, 'reviews/game.html', context=context_dict)


def add_review(request, game_slug):
    try:
        game = Game.objects.get(slug=game_slug)
    except Game.DoesNotExist:
        return restricted(request, status=404, message="The game you're looking for doesn't exist")

    if request.method == 'POST':
        review_form = ReviewForm(request.POST, request.user, game)
        if review_form.is_valid():
            # Save review to database
            review = review_form.save(commit=False)
            review.poster = request.user
            review.game = game
            review.save()
            messages.success(request, "Your review has been added")

            # Update stored average rating
            game.average_rating = (game.average_rating * game.number_ratings + int(review.rating)) / (game.number_ratings + 1)
            game.number_ratings += 1
            game.save()

            print(review.id)

            return HttpResponseRedirect(reverse('game', kwargs={'game_slug': game_slug}))
        else:
            messages.error(request, "You submitted an invalid review")
            review_form = ReviewForm(request.GET, request.user, game)
    else:
        review_form = ReviewForm(request.GET, request.user, game)

    context_dict = {'heading': "Add Review", 'review_form': review_form,
                    'slug': game_slug}
    return render(request, 'reviews/review.html', context=context_dict)


# @login_required
def profile(request, username):
    context_dict = {'heading': username}

    try:
        # Check if user is exists
        user = User.objects.get(username=username)

        # Obtain user's profile
        try:
            profile = UserProfile.objects.get(user=user)
            context_dict['profile'] = profile
        except UserProfile.DoesNotExist:
            context_dict['profile'] = None

        # Add any reviews and comments by user
        try:
            reviews = Review.objects.filter(poster=user).order_by('-post_datetime')
            context_dict['reviews'] = reviews
        except Review.DoesNotExist:
            context_dict['reviews'] = None
        try:
            comments = Comment.objects.filter(poster=user).order_by('-post_datetime')
            context_dict['comments'] = comments
        except Comment.DoesNotExist:
            context_dict['comments'] = None

    except User.DoesNotExist:
        return restricted(request, status=404, message="This user does not exist.")

    return render(request, 'reviews/profile.html', context=context_dict)


def edit_profile(request, username):
    try:
        user = User.objects.get(username=username)
        user_form = UserForm()
        profile_form = UserProfileForm()

        personal = [profile_form['display_name'],
            user_form['email'], profile_form['date_of_birth']]
        #personal[1].widget.attrs.update({'placeholder': user.email})
        password = [user_form['password'],
            user_form['password_confirm']]
        profile_image = profile_form['profile_image']
        biography = profile_form['biography']

        context_dict = {'heading': "Edit Profile",
            'personal': personal, 'password': password,
            'profile_image': profile_image, 'biography': biography}

    except User.DoesNotExist:
        return restricted(request, status=404, message="This user does not exist.")

    # If form has been submitted
    #if request.method == 'POST':
    #    user_form = UserForm(data=request.POST)
    #    profile_form = UserProfileForm(data=request.POST)

        # Check for form field validity
    #    if user_form.is_valid():
    #        user_form.save(commit=True)
    #        profile_form.save(commit=True)
    #        messages.success(request, "Your profile has been edited")
    #        return HttpResponseRedirect(reverse('profile', kwargs={'username': username}))
    #    else:
    #        messages.error(request, "Some fields contain errors.")
    #        user_form = UserForm(data=request.POST)
    #        profile_form = UserProfileForm(data=request.POST)

    # Otherwise, display form
    #else:
    #    user_form = UserForm()
    #    profile_form = UserProfileForm()

    #context_dict['user_form'] = user_form
    #context_dict['profile_form'] = profile_form

    return render(request, 'reviews/edit.html', context=context_dict)

def edit_personal(request, username):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # Check for form field validity
        if profile_form['display_name'].is_valid():
            #user_form.save(commit=True)
            #profile_form.save(commit=True)
            messages.success(request, "Your profile has been edited")
            return HttpResponseRedirect(reverse('profile', kwargs={'username': username}))
        else:
            messages.error(request, "Some fields contain errors.")
            #user_form = UserForm(data=request.POST)
            #profile_form = UserProfileForm(data=request.POST)

    # Otherwise
    #else:
    return HttpResponseRedirect(reverse('edit_profile', kwargs={'username': username}))
    #return render(request, 'reviews/edit.html', context=context_dict)

def edit_password(request, username):
    return render(request, 'reviews/edit.html', context=context_dict)


def register(request):
    if request.user.is_authenticated():
        messages.warning(request, "You can't register when you're logged in")
        return HttpResponseRedirect(reverse('index'))

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            messages.success(request, "Your account has been created")
            return HttpResponseRedirect(reverse('login'))

        else:
            messages.error(request, "You submitted an invalid registration form")
            user_form = UserForm(data=request.POST)

    else:
        user_form = UserForm()

    context_dict = {'heading': "Register", 'user_form': user_form}
    return render(request, 'reviews/register.html', context=context_dict)


def user_login(request):
    if request.user.is_authenticated():
        messages.warning(request, "You are already logged in")
        return HttpResponseRedirect(reverse('index'))

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
