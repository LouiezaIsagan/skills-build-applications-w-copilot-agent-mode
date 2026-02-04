from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Team, Activity, Workout, Leaderboard

class ModelTests(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name='Test Team')
        self.user = get_user_model().objects.create_user(username='testuser', email='test@example.com', password='testpass')
        self.activity = Activity.objects.create(user=self.user, type='run', duration=30)
        self.workout = Workout.objects.create(user=self.user, name='Test Workout', description='desc')
        self.leaderboard = Leaderboard.objects.create(team=self.team, points=10)

    def test_team_str(self):
        self.assertEqual(str(self.team), 'Test Team')

    def test_activity_str(self):
        self.assertIn('testuser', str(self.activity))

    def test_workout_str(self):
        self.assertIn('Test Workout', str(self.workout))

    def test_leaderboard_str(self):
        self.assertIn('Test Team', str(self.leaderboard))
