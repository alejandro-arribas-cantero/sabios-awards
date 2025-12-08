from django.shortcuts import render, redirect, get_object_or_404
# Trigger reload
from django.views import View
from django.contrib import messages
from django.utils import timezone
from .models import VotingPeriod, Candidate, Vote
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.dashboard.models import log_activity

class VoteView(LoginRequiredMixin, View):
    template_name = 'voting/vote.html'

    def get(self, request, period_id=None):
        now = timezone.now()
        
        if period_id:
            period = get_object_or_404(VotingPeriod, id=period_id, status='OPEN')
        else:
            # Find any active period
            period = VotingPeriod.objects.filter(status='OPEN').first()

        if not period:
            return render(request, 'voting/no_vote.html', {'message': 'No hay votación activa en este momento.'})

        # Check if user voted for this specific period
        if Vote.objects.filter(user=request.user, period=period).exists():
            return render(request, 'voting/already_voted.html', {'period': period})

        candidates = period.candidates.all()
        return render(request, self.template_name, {'period': period, 'candidates': candidates})

    def post(self, request, period_id=None):
        if period_id:
            period = get_object_or_404(VotingPeriod, id=period_id, status='OPEN')
        else:
            period = VotingPeriod.objects.filter(status='OPEN').first()

        if not period:
            messages.error(request, "La votación ha cerrado o no existe.")
            return redirect('dashboard')

        if Vote.objects.filter(user=request.user, period=period).exists():
            messages.warning(request, "Ya has votado en este periodo.")
            return redirect('dashboard')

        candidate_id = request.POST.get('candidate')
        candidate = get_object_or_404(Candidate, id=candidate_id, period=period)

        Vote.objects.create(user=request.user, period=period, candidate=candidate)
        log_activity(request.user, 'VOTE', f"Votó por {candidate.name} en {period}")
        messages.success(request, "¡Tu voto ha sido registrado!")
        return redirect('dashboard')

class ResultsView(LoginRequiredMixin, View):
    template_name = 'voting/results.html'

    def get(self, request, period_id=None):
        if period_id:
            period = get_object_or_404(VotingPeriod, id=period_id)
        else:
            # Default to latest revealed or closed
            period = VotingPeriod.objects.exclude(status='OPEN').order_by('-year', '-month').first()

        if not period:
             return render(request, 'voting/no_results.html')
        
        can_view = False
        if request.user.is_staff:
            can_view = True
        elif period.status == 'REVEALED':
            can_view = True
        # Removed logic that allowed voters to see OPEN/CLOSED results
        
        if not can_view:
            messages.error(request, "Aún no puedes ver los resultados de esta votación.")
            return redirect('dashboard')

        candidates = period.candidates.all()
        total_votes = period.votes.count()
        
        # Calculate stats
        stats = []
        for c in candidates:
            stats.append({
                'candidate': c,
                'votes': c.vote_count,
                'percentage': c.percentage
            })
        
        stats.sort(key=lambda x: x['votes'], reverse=True)

        return render(request, self.template_name, {
            'period': period,
            'stats': stats,
            'total_votes': total_votes
        })

class HallOfFameView(View):
    template_name = 'voting/hall_of_fame.html'

    def get(self, request):
        # Get all revealed periods with a winner photo
        legends = VotingPeriod.objects.filter(
            status='REVEALED'
        ).order_by('-year', '-month')
        
        return render(request, self.template_name, {'legends': legends})
