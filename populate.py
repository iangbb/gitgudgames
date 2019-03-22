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
            "name": "Shadow of the Tomb Raider",
            "description": "As Lara Croft races to save the world from a Mayan apocalypse, she must become the Tomb Raider she is destined to be.",
            "release_date": datetime.date(2019, 9, 14),
            "publisher": "Square Enix",
            "developer": "Eidos Montréal",
            "platform": Game.PC,
            "genre": Game.ADVENTURE,
            "average_rating": 3.5,
            "number_reviews": 2,
        },
        {
            "name": "Half Life 2",
            "description": "Dr. Freeman is taken out of stasis by his 'employer' to help rid the planet of invading aliens forces known as the Combine that entered through the portals he helped create.",
            "release_date": datetime.date(2004, 11, 16),
            "publisher": "Valve",
            "developer": "Valve",
            "platform": Game.PC,
            "genre": Game.SHOOTER,
            "average_rating": 3.75,
            "number_reviews": 4,
            "age_rating": "15",
        },
        {
            "name": "Dark Souls",
            "description": "After escaping an asylum, an undead warrior treks through the dangerous kingdom of Lordran.",
            "release_date": datetime.date(2012, 2, 24),
            "publisher": "BANDAI NAMCO Entertainment",
            "developer": "FromSoftware",
            "platform": Game.PS4,
            "genre": Game.ACTION,
            "average_rating": 4,
            "number_reviews": 3,
        },
    ]

    # Creates some users with randomly generated passwords
    users = [
        {
            "username": "iMakeannoyingComments",
            "password": generate_password(),
            "journalist": False,
        },
        {
            "username": "imAJournalist",
            "password": generate_password(),
            "journalist": True,
        },
        {
            "username": "gabeNewell",
            "password": generate_password(),
            "journalist": False,
        },
        {
            "username": "timSweeny",
            "password": generate_password(),
            "journalist": False,
        },
        {
            "username": "toddHoward",
            "password": generate_password(),
            "journalist": False,
        },
        {
            "username": "angryJoe",
            "password": generate_password(),
            "journalist": True,
        },
        {
            "username": "bigKeith",
            "password": generate_password(),
            "journalist": False,
        },
        {
            "username": "zeroPunctuation",
            "password": generate_password(),
            "journalist": True,
        },
        {
            "username": "pewDiePie",
            "password": generate_password(),
            "journalist": False,
        },
        {
            "username": "ian",
            "password": generate_password(),
            "journalist" : False,
        },
        {
            "username": "charles",
            "password": generate_password(),
            "journalist" : False,
        },
        {
            "username": "scott",
            "password": generate_password(),
            "journalist" : False,
        },
        {
            "username": "matthew",
            "password": generate_password(),
            "journalist" : False,
        },
    ]

    # TODO: actual review text
    reviews = [
        {
            "poster": "bigKeith",
            "game": "Dark Souls",
            "review_text": "Almost as hard as the brexit I want!",
            "rating": Review.FOUR_STARS,
        },
        {
            "poster": "gabeNewell",
            "game": "Half Life 2",
            "review_text": "Doesn't need a sequel",
            "rating": Review.FIVE_STARS,
        },
        {
            "poster": "zeroPunctuation",
            "game": "Half Life 2",
            "review_text": "This game was excellent however it had an unsatisfying ending",
            "rating": Review.FOUR_STARS,
        },
        {
            "poster": "toddHoward",
            "game": "Half Life 2",
            "review_text": "Not as good as Fallout 76",
            "rating": Review.ONE_STAR,
        },
        {
            "poster": "bigKeith",
            "game": "Half Life 2",
            "review_text": "Would've done better if set in Britain",
            "rating": Review.FOUR_STARS,
        },
        {
            "poster": "pewDiePie",
            "game": "Dark Souls",
            "review_text": "IT'S JUST LIKE DARK SOULS",
            "rating": Review.FOUR_STARS,
        },
        {
            "poster": "angryJoe",
            "game": "Dark Souls",
            "review_text": "This game makes me angry 😡",
            "rating": Review.THREE_STARS,
        },
        {
            "poster": "timSweeny",
            "game": "Dark Souls",
            "review_text": "Would've done better if it was on the Epic Games Store",
            "rating": Review.ONE_STAR,
        },
        {
            "poster": "imAJournalist",
            "game": "Shadow of the Tomb Raider",
            "review_text": "This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This isa good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is agood game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good gameThis is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game This is a good game",
            "rating": Review.FIVE_STARS,
        },
        {
            "poster": "bigKeith",
            "game": "Shadow of the Tomb Raider",
            "review_text": "I love that lara is a proud British Lass but game would've been better if set in Britain",
            "rating": Review.TWO_STARS,
        }

    ]

    # TODO: at least add some images when populating - should be easier to add than comments
    images = [
    {
        "poster" : "imAJournalist",
        "game" : "Shadow of the Tomb Raider",
        "image" : "/game_images/shadow_of_the_tomb_raider_1.jpg",
    },
    {
        "poster" : "imAJournalist",
        "game" : "Shadow of the Tomb Raider",
        "image" : "/game_images/shadow_of_the_tomb_raider_2.jpg",
    },
    {
        "poster" : "imAJournalist",
        "game" : "Shadow of the Tomb Raider",
        "image" : "/game_images/shadow_of_the_tomb_raider_3.jpg",
    },
    {
        "poster" : "imAJournalist",
        "game" : "Shadow of the Tomb Raider",
        "image" : "/game_images/shadow_of_the_tomb_raider_4.jpg",
    },
    {
        "poster" : "angryJoe",
        "game" : "Dark Souls",
        "image" : "/game_images/darksouls_1.jpg",
    },
    {
        "poster" : "angryJoe",
        "game" : "Dark Souls",
        "image" : "/game_images/darksouls_2.jpg",
    },
    {
        "poster" : "angryJoe",
        "game" : "Dark Souls",
        "image" : "/game_images/darksouls_3.jpg",
    },
    {
        "poster" : "angryJoe",
        "game" : "Dark Souls",
        "image" : "/game_images/darksouls_4.jpg",
    },
    {
        "poster" : "zeroPunctuation",
        "game" : "Half Life 2",
        "image" : "/game_images/half_life_1.jpg",
    },
    {
        "poster" : "zeroPunctuation",
        "game" : "Half Life 2",
        "image" : "/game_images/half_life_2.jpg",
    },
    {
        "poster" : "zeroPunctuation",
        "game" : "Half Life 2",
        "image" : "/game_images/half_life_3.jpg",
    },
    {
        "poster" : "zeroPunctuation",
        "game" : "Half Life 2",
        "image" : "/game_images/half_life_4.jpg",
    },
    ]

    comments = [
    {
        "poster": "bigKeith",
        "review": 2,
        "comment_text": "You are wrong Gabe",
    },
    {
        "poster": "zeroPunctuation",
        "review": 2,
        "comment_text": "The people need to know Gabe",
    },
    {
        "poster": "imAJournalist",
        "review": 2,
        "comment_text": "As a journalist you are wrong",
    },
    {
        "poster": "angryJoe",
        "review": 2,
        "comment_text": "I am i am indifferent towards this review",
    },
    {
        "poster": "pewDiePie",
        "review": 8,
        "comment_text": "Please subscribe",
    },

]

    for game in games:
        add_game(game)

    for user in users:
        add_user(user)

    for review in reviews:
        add_review(review)

    for comment in comments:
        add_comment(comment)

    for image in images:
        add_image(image)


def add_game(game):
    game_object = Game(name=game["name"], description=game["description"],
                                             releaseDate=game["release_date"], publisher=game["publisher"],
                                             developer=game["developer"], platform=game["platform"],
                                             genre=game["genre"], average_rating=game["average_rating"],
                                             number_ratings=game["number_reviews"])
    if game.get("age_rating"):
        game_object.age_rating = game["age_rating"]

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
        Review.objects.get_or_create(poster=user, game=game, review_text=review["review_text"],
                                     rating=review["rating"])[0]
    review_object.save()

    return review_object

def add_comment(comment):
    user = User.objects.get(username=comment["poster"])
    review = Review.objects.get(id=comment["review"])
    comment = \
        Comment.objects.get_or_create(poster=user, review=review, comment_text=comment["comment_text"])[0]

    comment.save()

    return comment

def add_image(image):
    game = Game.objects.get(name=image['game'])
    image = Image(game=game,image=image['image'])

    image.save()

    return image


# Randomly generates 16 character passwords
def generate_password():
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16))


if __name__ == '__main__':
    print("Populating database")
    populate()
