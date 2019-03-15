from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class Game(models.Model):
    PC = 'PC'
    XB1 = 'xb1'
    PS4 = 'ps4'
    SWI = 'swi'

    PLATFORM = (
        (PC, 'PC'),
        (XB1, 'Xbox One'),
        (PS4, 'Playstation 4'),
        (SWI, 'Switch'),
    )

    ACTION = 'Act'
    ADVENTURE = 'Adv'
    SHOOTER = 'Sho'

    GENRE = (
        (ACTION, 'Action'),
        (ADVENTURE, 'Adventure'),
        (SHOOTER, 'Shooter'),
    )

    AGE_12 = '12'
    AGE_16 = '16'
    AGE_18 = '18'

    AGE_RATING = (
        (AGE_12, '12'),
        (AGE_16, '16'),
        (AGE_18, '18'),
    )

    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=200)
    releaseDate = models.DateField()
    publisher = models.CharField(max_length=30)
    developer = models.CharField(max_length=30)
    platform = models.CharField(max_length=3, choices=PLATFORM, default=PC)
    genre = models.CharField(max_length=3, choices=GENRE, default=ACTION)
    age_rating = models.CharField(max_length=2, choices=AGE_RATING, null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    average_rating = models.DecimalField(max_digits=10, decimal_places=9, default=0)
    number_ratings = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Game, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    display_name = models.CharField(max_length=128, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images', blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    biography = models.CharField(max_length=1000, blank=True)
    is_journalist = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Review(models.Model):
    ONE_STAR = '1'
    TWO_STARS = '2'
    THREE_STARS = '3'
    FOUR_STARS = '4'
    FIVE_STARS = '5'

    RATINGS = (
        (ONE_STAR, '1'),
        (TWO_STARS, '2'),
        (THREE_STARS, '3'),
        (FOUR_STARS, '4'),
        (FIVE_STARS, '5'),
    )

    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    review_text = models.CharField(max_length=2000)
    rating = models.CharField(max_length=1, choices=RATINGS, default=ONE_STAR)
    post_datetime = models.DateTimeField(auto_now=False, auto_now_add=True)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.poster.username + " - " + self.game.name + " - " + str(self.post_datetime)


class Comment(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=200)
    post_datetime = models.DateTimeField(auto_now=False, auto_now_add=True)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.poster.username + " - " + self.review.game.name + " - " + str(self.post_datetime)


class Image(models.Model):
    poster = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='game_images')

    def __str__(self):
        return self.poster.username + " - " + self.game.name


class AbstractRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    upvote = models.BooleanField()  # false means this is a downvote

    class Meta:
        abstract = True


class CommentRating(AbstractRating):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + " - " + str(self.comment.post_datetime)


class ReviewRating(AbstractRating):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + " - " + str(self.review.post_datetime)
