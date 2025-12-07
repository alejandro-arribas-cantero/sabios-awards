from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import VotingPeriod, Candidate, Vote
from django.core.exceptions import ValidationError
from django.utils import timezone

class VotingTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.period = VotingPeriod.objects.create(month=1, year=2024, status='OPEN')
        self.candidate = Candidate.objects.create(period=self.period, name='Candidate 1')

    def test_vote_creation(self):
        vote = Vote.objects.create(user=self.user, period=self.period, candidate=self.candidate)
        self.assertEqual(Vote.objects.count(), 1)

    def test_one_vote_per_user_per_period(self):
        Vote.objects.create(user=self.user, period=self.period, candidate=self.candidate)
        with self.assertRaises(Exception): # IntegrityError or ValidationError depending on database
            Vote.objects.create(user=self.user, period=self.period, candidate=self.candidate)

    def test_cannot_vote_closed_period(self):
        self.period.status = 'CLOSED'
        self.period.save()
        vote = Vote(user=self.user, period=self.period, candidate=self.candidate)
        with self.assertRaises(ValidationError):
            vote.save()

    def test_candidate_must_belong_to_period(self):
        other_period = VotingPeriod.objects.create(month=2, year=2024, status='OPEN')
        other_candidate = Candidate.objects.create(period=other_period, name='Candidate 2')
        
        vote = Vote(user=self.user, period=self.period, candidate=other_candidate)
        with self.assertRaises(ValidationError):
            vote.save()

class ViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.period = VotingPeriod.objects.create(month=timezone.now().month, year=timezone.now().year, status='OPEN')
        self.candidate = Candidate.objects.create(period=self.period, name='Candidate 1')

    def test_vote_view_get(self):
        response = self.client.get(reverse('cast_vote'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Candidate 1')

    def test_vote_view_post(self):
        response = self.client.post(reverse('cast_vote'), {'candidate': self.candidate.id})
        self.assertEqual(Vote.objects.count(), 1)
        self.assertRedirects(response, reverse('dashboard'))

    def test_vote_view_already_voted(self):
        Vote.objects.create(user=self.user, period=self.period, candidate=self.candidate)
        response = self.client.get(reverse('cast_vote'))
        self.assertContains(response, 'Ya has votado')
