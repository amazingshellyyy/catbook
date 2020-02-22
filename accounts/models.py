from django.db import models
from django.contrib.auth.models import User

# one to one relationship
class Profile(models.Model):
    # CASCADE means if the user is deleted the profile is deleted
    # However, If the profile is deleted, the user is not deleted.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} Profile'

      