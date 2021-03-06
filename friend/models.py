from django.db import models
from django.contrib.auth.models import User

""" Model for Friend """
class Friend(models.Model):

    # Relationship between Friend and User is "many to one"
    user = models.ForeignKey(
        to=User,
        verbose_name='User',
        on_delete=models.CASCADE
    )

    friend_name = models.CharField(
        verbose_name='Friend Name',
        max_length=200,
    )

    birth_day = models.DateField(
        verbose_name='Birth Day',
        blank=True,
        null=True
    )

    memo = models.TextField(
        verbose_name='Memo',
        max_length=500,
        blank=True,
        null=True
    )
    
    photo = models.ImageField(
        verbose_name='Photo',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name_plural='Friend'

    def __str__(self):
        return self.friend_name