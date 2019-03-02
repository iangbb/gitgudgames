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

    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=200)
    releaseDate = models.DateField()
    publisher = models.CharField(max_length=30)
    developer = models.CharField(max_length=30)
    platform = models.CharField(max_length=3, choices=PLATFORM,default=PC)
    genre = models.CharField(max_length=3, choices=GENRE, default=ACTION)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Game, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    profile_image = models.ImageField(upload_to='profile_images', blank=True)
    date_of_birth = models.DateField(blank=True)
    biography = models.CharField(max_length=1000, blank=True)
    is_journalist = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
