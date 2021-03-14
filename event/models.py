from django.db import models
from django.contrib.auth.models import User
from friend.models import Friend

""" Model for Event """
class Event(models.Model):
    
    # Relationship between Event and User is "many to one"
    user = models.ForeignKey(
        to=User,
        verbose_name='User',
        on_delete=models.CASCADE
    )

    # Relationship between Event and Friend is "many to many"
    friend_name = models.ManyToManyField(
        to=Friend,
        blank=True,
    )

    event_name = models.CharField(
        verbose_name='Event Name',
        max_length=200
    )

    date = models.DateField(
        verbose_name='Date',
    )

    place = models.CharField(
        verbose_name='Place',
        max_length=200,
        blank=True,
        null=True
    )
    
    memo = models.TextField(
        verbose_name='Memo',
        max_length=500,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name_plural='Event'
    
    def __str__(self):
        return self.event_name