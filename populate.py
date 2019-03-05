import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gitgudgames.settings')

import django

django.setup()

import datetime
import random
import string
from reviews.models import *
from django.contrib.auth.models import User


def populate():
    # TODO: substitute some actual games in here
    games = [
        {
            "name": "An Action Game",
            "description": "This game has a lot of action",
            "release_date": datetime.date(2019, 1, 1),
            "publisher": "a game publisher",
            "developer": "a game developer",
            "platform": Game.PC,
            "genre": Game.ACTION,
        },
        {
            "name": "An Adventure Game",
            "description": "This game has a lot of adventure",
            "release_date": datetime.date(2018, 1, 1),
            "publisher": "a different game publisher",
            "developer": "a game developer",
            "platform": Game.PS4,
            "genre": Game.ADVENTURE,
        },
        {
            "name": "A Shooter Game",
            "description": "This game has a lot of shooting",
            "release_date": datetime.date(2018, 6, 1),
            "publisher": "a game publisher",
            "developer": "a different game developer",
            "platform": Game.XB1,
            "genre": Game.SHOOTER,
        },
    ]

    # Creates some users with randomly generated passwords
    users = [
        {
            "username": "ireviewgames",
            "password": generate_password(),
            "journalist": False,
        },
        {
            "username": "imajournalist",
            "password": generate_password(),
            "journalist": True,
        },
        {
            "username": "ijustmakeannoyingcomments",
            "password": generate_password(),
            "journalist": False,
        }
    ]

    # TODO: actual review text
    reviews = [
        {
            "poster": "ireviewgames",
            "game": "An Action Game",
            "review_text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc convallis mauris a tortor luctus venenatis. Vivamus ultricies ante lectus. Integer placerat tellus orci, nec cursus dolor finibus posuere.",
            "rating": Review.FIVE_STARS,
        },
        {
            "poster": "imajournalist",
            "game": "An Action Game",
            "review_text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed sed magna vel metus eleifend vehicula in id turpis. In neque neque, fringilla in lectus a, ultricies rutrum ante. Donec aliquet in quam quis mollis. Maecenas vestibulum purus ligula, at venenatis nibh finibus ut. In nec lacinia quam. Donec dictum lorem a dui accumsan hendrerit. Phasellus rutrum nisi erat, ut volutpat nibh viverra et. Nulla elementum nibh mattis blandit finibus. Vestibulum eget porta odio. Suspendisse vitae elit nullam.",
            "rating": Review.FOUR_STARS,
        },
        {
            "poster": "ireviewgames",
            "game": "An Adventure Game",
            "review_text": "something that isn't lorem ipsum",
            "rating": Review.ONE_STAR,
        }
    ]

    # TODO: at least add some images when populating - should be easier to add than comments
    comments = []
    images = []

    for game in games:
        add_game(game)

    for user in users:
        add_user(user)

    for review in reviews:
        add_review(review)


def add_game(game):
    game_object = Game.objects.get_or_create(name=game["name"], description=game["description"],
                                             releaseDate=game["release_date"], publisher=game["publisher"],
                                             developer=game["developer"], platform=game["platform"],
                                             genre=game["genre"])[0]
    game_object.save()
    return game_object


def add_user(user):
    user_object = User.objects.get_or_create(username=user["username"])[0]
    user_object.set_password(user["password"])
    user_object.save()

    print(user["username"])
    print(user["password"])

    user_profile_object = UserProfile.objects.get_or_create(user=user_object, is_journalist=user["journalist"])[0]
    user_profile_object.save()

    return user_object, user_profile_object


def add_review(review):
    user = User.objects.get(username=review["poster"])
    game = Game.objects.get(name=review["game"])
    review_object = \
    Review.objects.get_or_create(poster=user, game=game, review_text=review["review_text"], rating=review["rating"])[0]
    review_object.save()

    return review_object


# Randomly generates 16 character passwords
def generate_password():
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16))


if __name__ == '__main__':
    print("Populating database")
    populate()
