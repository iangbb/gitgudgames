from django.contrib import admin
from reviews.models import *

admin.site.register(Game)
admin.site.register(UserProfile)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(Image)
admin.site.register(CommentRating)
admin.site.register(ReviewRating)
