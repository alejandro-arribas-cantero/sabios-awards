from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Count
from .models import VotingPeriod, Candidate, Vote
from .forms import VotingPeriodForm, CandidateForm # Need to create forms

class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class AdminDashboardView(AdminRequiredMixin, TemplateView):
    template_name = 'voting/admin/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['periods'] = VotingPeriod.objects.all()[:5]
        context['total_votes'] = Vote.objects.count()
        context['total_candidates'] = Candidate.objects.values('name').distinct().count()
        return context

class VotingPeriodListView(AdminRequiredMixin, ListView):
    model = VotingPeriod
    template_name = 'voting/admin/period_list.html'
    context_object_name = 'periods'

class VotingPeriodCreateView(AdminRequiredMixin, CreateView):
    model = VotingPeriod
    form_class = VotingPeriodForm
    template_name = 'voting/admin/period_form.html'
    success_url = reverse_lazy('admin_period_list')

class VotingPeriodUpdateView(AdminRequiredMixin, UpdateView):
    model = VotingPeriod
    form_class = VotingPeriodForm
    template_name = 'voting/admin/period_form.html'
    success_url = reverse_lazy('admin_period_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            context['candidates'] = self.object.candidates.all()
        return context

class VotingPeriodDeleteView(AdminRequiredMixin, DeleteView):
    model = VotingPeriod
    template_name = 'voting/admin/period_confirm_delete.html'
    success_url = reverse_lazy('admin_period_list')

class CandidateCreateView(AdminRequiredMixin, CreateView):
    model = Candidate
    form_class = CandidateForm
    template_name = 'voting/admin/candidate_form.html'
    
    def get_success_url(self):
        return reverse_lazy('admin_period_update', kwargs={'pk': self.object.period.pk})

    def get_initial(self):
        # DEBUG: Check storage settings with ERROR level to force visibility
        import logging
        import os
        from django.conf import settings
        logger = logging.getLogger(__name__)
        
        storage = getattr(settings, 'DEFAULT_FILE_STORAGE', 'NOT SET')
        c_url = os.environ.get('CLOUDINARY_URL', 'MISSING')
        if c_url != 'MISSING':
             c_url = c_url[:15] + "..." # Mask it
        
        logger.error(f"🔥 DEBUG PROBE: STORAGE={storage} | CLOUDINARY_URL={c_url}")
        
        initial = super().get_initial()
        period_id = self.kwargs.get('period_id')
        if period_id:
            initial['period'] = period_id
        return initial

class CandidateDeleteView(AdminRequiredMixin, DeleteView):
    model = Candidate
    template_name = 'voting/admin/candidate_confirm_delete.html'
    
    def get_success_url(self):
        return reverse_lazy('admin_period_update', kwargs={'pk': self.object.period.pk})

class StatsView(AdminRequiredMixin, TemplateView):
    template_name = 'voting/admin/stats.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Simple stats
        context['votes_by_month'] = VotingPeriod.objects.annotate(total_votes=Count('votes')).order_by('year', 'month')
        
        # Best candidate of the year (most votes in a single period)
        # This is complex with SQLite/Django ORM efficiently, but we can iterate or use subqueries.
        # Simplest:
        candidates = Candidate.objects.annotate(num_votes=Count('votes')).order_by('-num_votes')[:5]
        context['top_candidates'] = candidates
        
        # Users who vote most
        users = Vote.objects.values('user__username').annotate(total=Count('id')).order_by('-total')[:10]
        context['top_voters'] = users
        
        return context
