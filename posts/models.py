""" Post Models. """

# Django
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    """Post Model"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey('users.Profile', on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='posts/photos')

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

class Like(models.Model):
    """Like Model"""

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey('users.Profile', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} by @{self.user.username}"
