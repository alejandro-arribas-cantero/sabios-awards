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

        context = {
            'current_period': current_period,
            'has_voted': has_voted,
            'last_winner_period': last_winner_period,
            'user_votes': user_votes,
            'is_admin': request.user.is_staff,
            'show_intro': show_intro
        }
        return render(request, self.template_name, context)
