from django.test import TestCase
from django.contrib.auth.models import User
from reviews.models import Game, UserProfile, Review, Comment, Image, CommentRating, ReviewRating
from datetime import date, timedelta


# Create your tests here.

# Models
class GameMethodTests(TestCase):
    def init_game(self, name):
        return Game(name=name, description='test', releaseDate=date.today(),
            publisher='test', developer='today', platform='test', genre='test',
            age_rating='13', price=1, average_rating=5, number_ratings=1, slug='test')

    def test_ensure_numeric_fields_are_positive(self):
        game = self.init_game("test")
        game.price = -1
        game.average_rating = -1
        game.number_ratings = -1
        game.save()
        self.assertEqual((game.price >= 0), True)
        self.assertEqual((game.average_rating >= 0), True)
        self.assertEqual((game.number_ratings >= 0), True)

    def test_ensure_slug_fields_works(self):
        game = self.init_game("Dark Souls")
        game.save()
        self.assertEqual((game.slug == "dark-souls"), True)

class UserProfileMethodTests(TestCase):
    def init_profile(self, username):
        user = User(username=username)
        user.save()
        return UserProfile(user=user, display_name='test',
            date_of_birth=date.today(),
            biography='test', is_journalist=False)

    def test_ensure_date_of_birth_is_not_future(self):
        profile = self.init_profile('test')
        profile.date_of_birth = date.today() + timedelta(days=1)
        profile.save()
        self.assertEqual((profile.date_of_birth <= date.today()), True)

class ReviewMethodTests(TestCase):
    def init_review(self, username, gamename):
        user = User(username=username)
        user.save()
        game = Game(name=gamename, releaseDate=date.today())
        game.save()
        return Review(poster=user, game=game, review_text='test',
            rating=1, post_datetime=date.today(), votes=1)

    def test_ensure_post_datetime_is_not_future(self):
        review = self.init_review('test', 'test')
        review.post_datetime += timedelta(days=1)
        review.save()
        self.assertEqual((review.post_datetime.date() <= date.today()), True)

    def test_ensure_numeric_fields_are_positive(self):
        review = self.init_review('test', 'test')
        review.votes = -1
        review.save()
        self.assertEqual((review.votes >= 0), True)

class CommentMethodTests(TestCase):
    def init_comment(self, username, reviewername, gamename):
        comment_user = User(username=username)
        comment_user.save()
        review_user = User(username=reviewername)
        review_user.save()
        game = Game(name=gamename, releaseDate=date.today())
        game.save()
        review = Review(poster=review_user, game=game, post_datetime=date.today())
        review.save()
        return Comment(poster=comment_user, review=review, comment_text='test',
            post_datetime=date.today(), votes=1)

    def test_ensure_post_datetime_is_not_future(self):
        comment = self.init_comment('test1', 'test2', 'test')
        comment.post_datetime += timedelta(days=1)
        comment.save()
        self.assertEqual((comment.post_datetime.date() <= date.today()), True)

    def test_ensure_numeric_fields_are_positive(self):
        comment = self.init_comment('test1', 'test2', 'test')
        comment.votes = -1
        comment.save()
        self.assertEqual((comment.votes >= 0), True)
