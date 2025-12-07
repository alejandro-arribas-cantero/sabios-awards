from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.voting.models import VotingPeriod, Candidate, Vote
from django.utils import timezone
from datetime import timedelta
import random

class Command(BaseCommand):
    help = 'Seeds initial data for the application'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # Create Users
        admin, _ = User.objects.get_or_create(username='admin', email='admin@example.com', is_staff=True, is_superuser=True)
        admin.set_password('admin')
        admin.save()
        
        user1, _ = User.objects.get_or_create(username='usuario', email='user@example.com')
        user1.set_password('usuario')
        user1.save()

        # Create Current Month Period
        now = timezone.now()
        current_period, created = VotingPeriod.objects.get_or_create(
            month=now.month,
            year=now.year,
            defaults={'status': 'OPEN'}
        )
        
        if created:
            candidates_names = ['Lionel Messi', 'Cristiano Ronaldo', 'Kylian Mbappé', 'Erling Haaland']
            for name in candidates_names:
                Candidate.objects.create(period=current_period, name=name)
            self.stdout.write(f'Created current period {current_period}')

        # Create Previous Month Period (Revealed)
        prev_date = now.replace(day=1) - timedelta(days=1)
        prev_period, created = VotingPeriod.objects.get_or_create(
            month=prev_date.month,
            year=prev_date.year,
            defaults={'status': 'OPEN'} # Start as OPEN to allow voting
        )
        
        if created:
            c1 = Candidate.objects.create(period=prev_period, name='Vinicius Jr')
            Candidate.objects.create(period=prev_period, name='Jude Bellingham')
            Candidate.objects.create(period=prev_period, name='Rodri')
            Candidate.objects.create(period=prev_period, name='Harry Kane')
            
            # Add some votes
            Vote.objects.create(user=admin, period=prev_period, candidate=c1)
            
            # Now update status
            prev_period.status = 'REVEALED'
            prev_period.save()
            
            self.stdout.write(f'Created previous period {prev_period}')

        self.stdout.write(self.style.SUCCESS('Successfully seeded data'))
