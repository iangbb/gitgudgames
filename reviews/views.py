from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from reviews.models import Game, Review, Comment, User, UserProfile, Image, Comment, ReviewRating, CommentRating
from reviews.forms import UserForm, UserProfileForm, ProfileImageForm, DetailsForm, PasswordForm, BiographyForm, ReviewForm


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
    platforms = [platform[1] for platform in Game.PLATFORM]  # Platform user-friendly names
    genres = [genre[1] for genre in Game.GENRE]  # Genre user-friendly names
    platforms_checked = []  # Track which platforms checkboxes are selected
    genres_checked = []

    if request.method == "POST":
        platform_options = []
        genre_options = []
        sorting_order = request.POST.get('order')

        # Find what platforms the user has selected
        for platform in Game.PLATFORM:
            if request.POST.get('platform-' + platform[1]):
                platform_options.append(platform[0])
                platforms_checked.append(platform[1])

        # Default to all platforms if not specified
        if len(platform_options) == 0:
            platform_options = [platform[0] for platform in Game.PLATFORM]

        # Same with genres
        for genre in Game.GENRE:
            if request.POST.get('genre-' + genre[1]):
                genre_options.append(genre[0])
                genres_checked.append(genre[1])

        if len(genre_options) == 0:
            genre_options = [genre[0] for genre in Game.GENRE]

        # Default sorting order is highest rated first
        if not sorting_order:
            sorting_order = '-average_rating'

        games = Game.objects.filter(genre__in=genre_options, platform__in=platform_options).order_by(sorting_order)
    else:
        games = Game.objects.all().order_by('-average_rating')
        sorting_order = '-average_rating'

    context_dict = {'heading': "Games", 'genres': genres, 'platforms': platforms, 'games': games,
                    'platforms_checked': platforms_checked, 'genres_checked': genres_checked, 'order': sorting_order}
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
        review_form = ReviewForm(data=request.POST)
        if review_form.is_valid():
            # Save review to database
            review = review_form.save(commit=False)
            review.poster = request.user
            review.game = game
            review.save()
            messages.success(request, "Your review has been added")

            # Update stored average rating
            game.average_rating = \
                (game.average_rating * game.number_ratings + int(review.rating)) / (game.number_ratings + 1)
            game.number_ratings += 1
            game.save()

            print(review.id)

            return HttpResponseRedirect(reverse('game', kwargs={'game_slug': game_slug}))
        else:
            messages.error(request, "You submitted an invalid review")
            review_form = ReviewForm()
    else:
        review_form = ReviewForm()

    context_dict = {'heading': "Add Review", 'review_form': review_form,
                    'slug': game_slug}
    return render(request, 'reviews/review.html', context=context_dict)


# @login_required
def profile(request, username):
    context_dict = {'heading': 'Profile of ' + username}

    try:
        # Check if user is exists
        user = User.objects.get(username=username)

        # Obtain user's profile
        try:
            profile = UserProfile.objects.get(user=user)
            context_dict['profile'] = profile
            if profile.display_name is not None:
                context_dict['heading'] = 'Profile of ' + profile.display_name

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

@login_required
def edit_profile(request, username):
    if request.method == 'POST':
        user = User.objects.get(username=username)
        # Image form
        if 'image_button' in request.POST:
            profile_image_form = ProfileImageForm(files=request.FILES)

            if profile_image_form.is_valid():
                profile = UserProfile.objects.get(user=user)
                profile.profile_image = request.FILES['profile_image']
                profile.save()
                messages.success(request, "Your profile picture has been changed.")
                return HttpResponseRedirect(reverse('profile', kwargs={'username': username}))
            else:
                messages.error(request, "Your submitted image was not valid.")
                return HttpResponseRedirect(reverse('edit_profile', kwargs={'username': username}))

        # Details form
        elif 'details_button' in request.POST:
            details_form = DetailsForm(data=request.POST)

            print(request.POST.get('date_of_birth'))
            print(str(details_form.data['date_of_birth']))

            # Check for form field validity
            if details_form.is_valid():
                profile = UserProfile.objects.get(user=user)
                profile.display_name = request.POST.get('display_name')
                user.email = request.POST.get('email')
                profile.date_of_birth = request.POST.get('date_of_birth')
                profile.save()
                user.save()
                messages.success(request, "Your profile has been edited")
                return HttpResponseRedirect(reverse('profile', kwargs={'username': username}))
            else:
                messages.error(request, "Some fields contain errors.")
                return HttpResponseRedirect(reverse('edit_profile', kwargs={'username': username}))

        # Password form
        elif 'password_button' in request.POST:
            # Add user's username to post
            password_form = PasswordForm(data=request.POST)

            if password_form.is_valid():
                user.set_password(password_form.data['password'])
                user.save()
                messages.success(request, "Your password has been changed")
                return HttpResponseRedirect(reverse('login'))
            else:
                messages.error(request, "Some fields contain errors.")
                return HttpResponseRedirect(reverse('edit_profile', kwargs={'username': username}))

        # Biography form
        elif 'biography_button' in request.POST:
            biography_form = BiographyForm(data=request.POST)

            if biography_form.is_valid():
                profile = UserProfile.objects.get(user=user)
                profile.biography = request.POST.get('biography')
                profile.save()
                messages.success(request, "Your biography has been updated.")
                return HttpResponseRedirect(reverse('profile', kwargs={'username': username}))
            else:
                messages.error(request, "Some fields contain errors.")
                return HttpResponseRedirect(reverse('edit_profile', kwargs={'username': username}))


    # Otherwise, load page
    else:
        try:
            user = User.objects.get(username=username)
            try:
                profile = UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExist:
                profile = None

            profile_image_form = ProfileImageForm()
            details_form = DetailsForm()
            password_form = PasswordForm()
            biography_form = BiographyForm()

            context_dict = {'heading': "Edit Profile", 'profile': profile,
                'profile_image_form': profile_image_form, 'details_form': details_form,
                'password_form': password_form, 'biography_form': biography_form }

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


# Gets up to 3 more comments for the given review, starting at the given index
def ajax_get_comments(request):
    review = request.GET.get('review')
    start = request.GET.get('start')

    # Ensure both fields have been provided
    if not review or not start:
        return ajax_error()

    start = int(start)
    json = {'number': 0, 'comments': [], 'more': False}
    # Retrieve comments for the given review, starting from index 'start'
    comments = Comment.objects.filter(review=review).order_by('-votes')[start:]

    # If comments have been found, generate the JSON to return to the client
    if len(comments) > 0:
        json['number'] = len(comments)
        json['comments'] = [comment.as_json() for comment in comments[:3]]  # Send next 3

        # If there are more comments to retrieve, then advise this to client
        if len(comments) > 3:
            json['more'] = True

    return JsonResponse(json)


# Gets up to 3 more reviews for the given game, starting at the given index
def ajax_get_reviews(request):
    game = request.GET.get('game')
    start = request.GET.get('start')

    # Ensure both fields have been provided
    if not game or not start:
        return ajax_error()

    start = int(start)
    json = {'number': 0, 'reviews': [], 'more': False}
    # Retrieve reviews for the given game, starting from index 'start'
    reviews = Review.objects.filter(game=game).order_by('-votes')[start:]

    # If reviews have been found, generate JSON
    if len(reviews) > 0:
        json['number'] = len(reviews)

        for review in reviews[:3]:
            comments = Comment.objects.filter(review=review).order_by('-votes')[:3]  # Get top 3 comments for review
            try:
                user_profile = UserProfile.objects.get(user=review.poster)
                profile_image_url = user_profile.profile_image.url
                json['reviews'].append(review.as_json(comments, profile_image_url))
            except UserProfile.DoesNotExist:
                print("No user profile found for " + review.poster)
                json['reviews'].append(review.as_json(comments))

        # Indicate if there are more reviews to retrieve
        if len(reviews) > 3:
            json['more'] = True

    return JsonResponse(json)


# Adds a comment to a review submitted via an AJAX POST request
def ajax_add_comment(request):
    # Ensure user is logged in before proceeding
    if not request.user.is_authenticated():
        return ajax_error(message="You must be logged in to comment", status=403)

    # Enforce POST method
    if request.method != 'POST':
        return ajax_error(message="A POST request was expected", status=405)

    review_id = request.POST.get('review')
    comment_text = request.POST.get('comment_text')

    # Confirm data has been provided
    if not review_id or not comment_text:
        return ajax_error()

    # Perform validation on comment text, returning JSON error if invalid
    if len(comment_text) == 0 or len(comment_text) > 200:
        return ajax_error(message="Comment text must be 1 to 200 characters long.")

    try:
        # Save comment
        review = Review.objects.get(id=int(review_id))
        comment = Comment(poster=request.user, review=review, comment_text=comment_text)
        comment.save()
        return JsonResponse({'success': True, 'comment': comment.as_json()})
    except Review.DoesNotExist:
        return ajax_error(message="Review does not exist", status=404)


# Upvotes or downvotes the given comment, or changes the user's vote on the comment
def ajax_rate_comment(request):
    # Must be logged in
    if not request.user.is_authenticated():
        return ajax_error(message="You must be logged in to comment", status=403)

    comment_id = request.GET.get('comment')
    upvote = request.GET.get('upvote')

    # Ensure both fields are given
    if not comment_id or not upvote:
        return ajax_error()

    comment_id = int(comment_id)
    upvote = upvote.lower() == "true"
    changed = False  # Used to track if the user has updated their vote

    try:
        comment = Comment.objects.get(id=comment_id)  # Retrieve the comment

        try:
            rating = CommentRating.objects.get(user=request.user, comment=comment)  # Search for existing rating

            # If the user has already voted on the comment and isn't changing their vote, then don't proceed
            if rating.upvote == upvote:
                return ajax_error(message="Already voted on this comment", status=403)
            else:
                # The user is changing their vote, so update their vote and the total votes on the comment
                rating.upvote = upvote
                rating.save()
                comment.votes += 2 if upvote else -2
                comment.save()
                changed = True
        except CommentRating.DoesNotExist:
            # The user has never voted on this comment before, so create a new object and save the rating
            rating = CommentRating(user=request.user, comment=comment, upvote=upvote)
            rating.save()
            comment.votes += 1 if upvote else -1
            comment.save()

        # Return a successful status report
        return JsonResponse({'success': True, 'comment': comment_id, 'upvote': upvote, 'changed': changed})
    except Comment.DoesNotExist:
        return ajax_error(message="Comment does not exist", status=404)


# Upvotes or downvotes the given review, or changes the user's vote on the comment
def ajax_rate_review(request):
    # Must be logged in
    if not request.user.is_authenticated():
        return ajax_error(message="You must be logged in to comment", status=403)

    review_id = request.GET.get('review')
    upvote = request.GET.get('upvote')

    # Ensure both fields are given
    if not review_id or not upvote:
        return ajax_error()

    review_id = int(review_id)
    upvote = upvote.lower() == "true"
    changed = False  # Used to track if the user has updated their vote

    try:
        review = Review.objects.get(id=review_id)  # Retrieve the review

        try:
            rating = ReviewRating.objects.get(user=request.user, review=review)  # Search for existing rating

            # If the user has already voted on the review and isn't changing their vote, then don't proceed
            if rating.upvote == upvote:
                return ajax_error(message="Already voted on this review", status=403)
            else:
                # The user is changing their vote, so update their vote and the total votes on the review
                rating.upvote = upvote
                rating.save()
                review.votes += 2 if upvote else -2
                review.save()
                changed = True
        except ReviewRating.DoesNotExist:
            # The user has never voted on this review before, so create a new object and save the rating
            rating = ReviewRating(user=request.user, review=review, upvote=upvote)
            rating.save()
            review.votes += 1 if upvote else -1
            review.save()

        # Return a successful status report
        return JsonResponse({'success': True, 'review': review_id, 'upvote': upvote, 'changed': changed})
    except Review.DoesNotExist:
        return ajax_error(message="Review does not exist", status=404)


# Returns an error as a JSON-encoded message with the given status code, defaulting to bad request
def ajax_error(message="Bad AJAX request data", status=400):
    return JsonResponse({'error': message}, status=status)
