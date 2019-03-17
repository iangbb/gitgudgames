from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
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
        # Filter only reviews relevant to this game
        reviews = Review.objects.filter(game=game).order_by('-votes')
        pictures = Image.objects.filter(game=game)

        # Find comments for each review and store in dictionary
        comments = {}
        for review in reviews:
            comments[review] = Comment.objects.filter(review=review).order_by('-votes')[:3]

        context_dict['game'] = game
        context_dict['reviews'] = reviews
        context_dict['pictures'] = pictures
        context_dict['comments'] = comments
    except Game.DoesNotExist:
        return restricted(request, status=404, message="The game you requested could not be found")

    return render(request, 'reviews/game.html', context=context_dict)


@login_required
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
    if request.method == 'POST':
        user = User.objects.get(username=username)
        # Image form
        if 'image_button' in request.POST:
            profile = UserProfile.objects.get(user=user)
            profile_form = UserProfileForm()

            file = request.FILES['profile_image']

            # Check for form field validity
            if profile_form.clean_profile_image(file):
                fs = FileSystemStorage("media/profile_images")
                filename = fs.save(file.name, file)
                profile.profile_image = filename
                profile.save()
                messages.success(request, "Your profile picture has been changed.")
            else:
                messages.error(request, "Some fields contain errors.")

            return HttpResponseRedirect(reverse('profile', kwargs={'username': username}))

        # Details form
        elif 'details_button' in request.POST:
            profile = UserProfile.objects.get(user=user)
            profile_form = UserProfileForm(data=request.POST)

            # Check for form field validity
            #if (profile_form.clean_display_name() and
                    #profile_form.clean_display_name()):
            if profile_form.clean_display_name():
                profile.display_name = request.POST.get('display_name')
                user.email = request.POST.get('email')
                #profile.date_of_birth = profile_form.data['date_of_birth']
                profile.save()
                user.save()
                messages.success(request, "Your profile has been edited")
            else:
                messages.error(request, "Some fields contain errors.")

            return HttpResponseRedirect(reverse('profile', kwargs={'username': username}))

        # Password form
        elif 'password_button' in request.POST:
            user_form = UserForm(data=request.POST)

            if user_form.clean_password():
                user.set_password(user_form.data['password'])
                user.save()
                messages.success(request, "Your password has been changed")
            else:
                messages.error(request, "Some fields contain errors.")

            return HttpResponseRedirect(reverse('profile', kwargs={'username': username}))

        # Biography form
        elif 'biography_button' in request.POST:
            profile = UserProfile.objects.get(user=user)
            profile_form = UserProfileForm(data=request.POST)

            if profile_form.clean_biography():
                profile.biography = request.POST.get('biography')
                profile.save()
                messages.success(request, "Your biography has been updated.")
            else:
                messages.error(request, "Some fields contain errors.")

            return HttpResponseRedirect(reverse('profile', kwargs={'username': username}))

    # Otherwise, load page
    else:
        try:
            user = User.objects.get(username=username)
            try:
                profile = UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExist:
                profile = None

            user_form = UserForm()
            profile_form = UserProfileForm()

            context_dict = {'heading': "Edit Profile", 'profile': profile,
                'user_form': user_form, 'profile_form': profile_form }

        except User.DoesNotExist:
            return restricted(request, status=404, message="This user does not exist.")

    return render(request, 'reviews/edit.html', context=context_dict)


def register(request):
    if request.user.is_authenticated():
        messages.warning(request, "You can't register when you're logged in")
        return HttpResponseRedirect(reverse('index'))

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            # Create user
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            # Create an associated profile for user
            profile = UserProfile.objects.get_or_create(user=user)[0]
            profile.save()

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
        next = request.POST.get('next')

        # For security, prevent cross-site redirection
        if next[:1] != '/' or next[:2] == '//':
            next = False

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                messages.success(request, "Logged in successfully")
                return HttpResponseRedirect(next if next else reverse('index'))
            else:
                messages.error(request, "Your account has been disabled")
                return HttpResponseRedirect(next if next else reverse('login'))

        else:
            messages.error(request, "Incorrect login details")
            response = HttpResponseRedirect(reverse('login'))

            # Re-append Django's next parameter, if it exists
            if next:
                response['Location'] += "?next=" + next

            return response

    context_dict = {'heading': "Login"}
    if request.GET.get('next'):
        context_dict['next'] = request.GET.get('next')

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
