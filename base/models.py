from django.db import models
from django.contrib.auth.models import AbstractUser
import time
from datetime import datetime
import uuid


class User(AbstractUser):
    name = models.CharField(max_length=255, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(default='avatar.png')
    id = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True, editable=False)
    hackathon_participants = models.BooleanField(default=True, null=True)
    
    USERNAME_FIELD ="email"
    REQUIRED_FIELDS = ['username']


class Event(models.Model):
    name = models.CharField(max_length=200)
    #preview = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, blank=True, related_name='events')
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    registration_deadline = models.DateTimeField(null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-end_date']

    # @property
    # def event_status(self):
    #     status = None
        
    #     present = datetime.now().timestamp()
    #     deadline = self.registration_deadline.timestamp()
    #     past_deadline = (present > deadline)

    #     if past_deadline:
    #         status = 'Finished'
    #     else:
    #         status = 'Ongoing'

    #     return status


class Submission(models.Model):
    participant = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="submissions")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    details = models.TextField(null=True, blank=False)
    id = models.UUIDField(default=uuid.uuid4, unique=True,   primary_key=True, editable=False)

    def __str__(self):
        return str(self.event) + ' --- ' + str(self.participant)
    
    