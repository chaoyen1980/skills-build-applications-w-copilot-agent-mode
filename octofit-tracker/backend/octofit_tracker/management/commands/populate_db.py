from django.core.management.base import BaseCommand
from tracker_app.models import User, Team, Activity, Leaderboard, Workout
from django.conf import settings
from pymongo import MongoClient
from datetime import timedelta
from bson import ObjectId

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activity, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Connect to MongoDB
        client = MongoClient(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT'])
        db = client[settings.DATABASES['default']['NAME']]

        # Drop existing collections
        db.users.drop()
        db.teams.drop()
        db.activity.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Clear existing data in the database before inserting new entries
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Create users
        users = [
            User(username='thundergod', email='thundergod@mhigh.edu', password='thundergodpassword'),
            User(username='metalgeek', email='metalgeek@mhigh.edu', password='metalgeekpassword'),
            User(username='zerocool', email='zerocool@mhigh.edu', password='zerocoolpassword'),
            User(username='crashoverride', email='crashoverride@hmhigh.edu', password='crashoverridepassword'),
            User(username='sleeptoken', email='sleeptoken@mhigh.edu', password='sleeptokenpassword'),
        ]
        User.objects.bulk_create(users)

        # Add more test data for teams, activities, leaderboard, and workouts
        teams = [
            Team(name='Team A'),
            Team(name='Team B')
        ]
        # Convert Django model instances to dictionaries before inserting into MongoDB
        db.teams.insert_many([{'name': team.name} for team in teams])

        activities = [
            Activity(user=users[0], description='Running', duration=timedelta(minutes=30), date='2025-04-10'),
            Activity(user=users[1], description='Cycling', duration=timedelta(minutes=45), date='2025-04-10')
        ]
        db.activity.insert_many([
            {
                'user_id': activity.user.id,
                'description': activity.description,
                'duration': activity.duration.total_seconds(),
                'date': str(activity.date)
            } for activity in activities
        ])

        leaderboard = [
            Leaderboard(team=teams[0], points=100),
            Leaderboard(team=teams[1], points=80)
        ]
        db.leaderboard.insert_many([
            {
                'team_id': entry.team.id,
                'points': entry.points
            } for entry in leaderboard
        ])

        workouts = [
            Workout(name='Morning Yoga', description='A relaxing yoga session', duration=timedelta(minutes=60)),
            Workout(name='HIIT', description='High-intensity interval training', duration=timedelta(minutes=30))
        ]
        db.workouts.insert_many([
            {
                'name': workout.name,
                'description': workout.description,
                'duration': workout.duration.total_seconds()
            } for workout in workouts
        ])

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))
