from django.db import models
from django.utils import timezone


class User(models.Model):
    email = models.EmailField(primary_key=True)
    REQUIRED_FIELDS = ()
    USERNAME_FIELD = 'email'
    last_login = models.DateTimeField(default=timezone.now)

    def is_authenticated(self):
        return True
