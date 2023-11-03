from colorfield.fields import ColorField
from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Location(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Profile(models.Model):
    color = ColorField(default='#720026')
    font_preference = models.CharField(max_length=50, default='Default')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.CharField(max_length=200, null=True, blank=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} Profile'


    def create_profile(sender, instance, created,kwargs):
        if created:
            Profile.objects.create(user=instance)


# Path: profile/admin.py
class UserVote(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    is_upvote = models.BooleanField(default=True)

    class Meta:
        unique_together = ('voter', 'profile')