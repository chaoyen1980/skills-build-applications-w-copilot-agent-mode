from django.db import models

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

class Team(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, related_name='teams')

class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    description = models.CharField(max_length=255)
    duration = models.DurationField()
    date = models.DateField()

class Leaderboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leaderboard_entries')
    points = models.IntegerField()

class Workout(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.DurationField()