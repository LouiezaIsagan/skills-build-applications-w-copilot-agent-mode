from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models

from octofit_tracker import models as octo_models

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Delete existing data
        get_user_model().objects.all().delete()
        octo_models.Team.objects.all().delete()
        octo_models.Activity.objects.all().delete()
        octo_models.Leaderboard.objects.all().delete()
        octo_models.Workout.objects.all().delete()

        # Create teams
        marvel = octo_models.Team.objects.create(name='Marvel')
        dc = octo_models.Team.objects.create(name='DC')

        # Create users (super heroes)
        users = [
            {'email': 'tony@stark.com', 'username': 'IronMan', 'team': marvel},
            {'email': 'steve@rogers.com', 'username': 'CaptainAmerica', 'team': marvel},
            {'email': 'bruce@wayne.com', 'username': 'Batman', 'team': dc},
            {'email': 'clark@kent.com', 'username': 'Superman', 'team': dc},
        ]
        user_objs = []
        for u in users:
            user = get_user_model().objects.create_user(email=u['email'], username=u['username'], password='password')
            user.profile.team = u['team']
            user.profile.save()
            user_objs.append(user)

        # Create activities
        for user in user_objs:
            octo_models.Activity.objects.create(user=user, type='run', duration=30)
            octo_models.Activity.objects.create(user=user, type='cycle', duration=45)

        # Create workouts
        for user in user_objs:
            octo_models.Workout.objects.create(user=user, name='Morning Cardio', description='Cardio session')

        # Create leaderboard
        for team in [marvel, dc]:
            octo_models.Leaderboard.objects.create(team=team, points=100)

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data'))
