from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from apps.voting.models import VotingPeriod, Vote
from datetime import timedelta

class DashboardView(LoginRequiredMixin, View):
    template_name = 'dashboard/index.html'

    def get(self, request):
        now = timezone.now()
        
        # 1. Check for Open Voting
        current_period = VotingPeriod.objects.filter(
            month=now.month, 
            year=now.year, 
            status='OPEN'
        ).first()
        
        has_voted = False
        if current_period:
            has_voted = Vote.objects.filter(user=request.user, period=current_period).exists()

        # 2. Previous Winner (Last REVEALED period)
        last_winner_period = VotingPeriod.objects.filter(status='REVEALED').order_by('-year', '-month').first()
        
        # 3. User History
        user_votes = Vote.objects.filter(user=request.user).order_by('-timestamp')[:5]

        # 4. Check for intro video flag
        show_intro = request.session.pop('show_intro', False)

        # 5. Community Stats
        from django.db.models import Count
        from django.contrib.auth.models import User
        
        top_voters = User.objects.filter(is_staff=False, is_active=True).annotate(total_votes=Count('votes')).order_by('-total_votes')[:3]
        most_logins = User.objects.filter(is_staff=False, is_active=True).select_related('profile').order_by('-profile__login_count')[:3]
        least_logins = User.objects.filter(is_staff=False, is_active=True).select_related('profile').order_by('profile__login_count')[:3]

        context = {
            'current_period': current_period,
            'has_voted': has_voted,
            'last_winner_period': last_winner_period,
            'user_votes': user_votes,
            'is_admin': request.user.is_staff,
            'show_intro': show_intro,
            'top_voters': top_voters,
            'most_logins': most_logins,
            'least_logins': least_logins,
        }
        return render(request, self.template_name, context)
