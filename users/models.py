"""Users Models"""
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    """ Profile Model
    
    Proxy model that extends the base data with order information 
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    website = models.URLField(max_length=500, blank=True)
    biography = models.TextField(blank=True)
    phone_number = models.CharField(max_length=20 ,blank=True)

    picture = models.ImageField(upload_to='users/pictures', blank=True, null=True)

    def followers(self):
        return Follows.objects.filter(
            followed=self
        ).count()

    def following(self):
        return Follows.objects.filter(
            follower=self
        ).count()

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

class Follows(models.Model):
    followed = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='followed',
    )
    follower = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='follower'
    )

    class Meta:
        unique_together = ('followed', 'follower',)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
