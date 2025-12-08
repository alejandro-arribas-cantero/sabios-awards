from django.urls import path
from .views import VoteView, ResultsView, HallOfFameView
from .views_admin import (
    AdminDashboardView, VotingPeriodListView, VotingPeriodCreateView, 
    VotingPeriodUpdateView, VotingPeriodDeleteView, CandidateCreateView, 
    CandidateUpdateView, CandidateDeleteView, StatsView, PopulateCandidatesView
)

urlpatterns = [
    path('cast/', VoteView.as_view(), name='cast_vote'),
    path('cast/<int:period_id>/', VoteView.as_view(), name='cast_vote_period'),
    path('results/', ResultsView.as_view(), name='latest_results'),
    path('results/<int:period_id>/', ResultsView.as_view(), name='period_results'),
    path('hall-of-fame/', HallOfFameView.as_view(), name='hall_of_fame'),
    
    # Admin URLs
    path('admin/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('admin/periods/', VotingPeriodListView.as_view(), name='admin_period_list'),
    path('admin/periods/create/', VotingPeriodCreateView.as_view(), name='admin_period_create'),
    path('admin/periods/<int:pk>/update/', VotingPeriodUpdateView.as_view(), name='admin_period_update'),
    path('admin/periods/<int:pk>/delete/', VotingPeriodDeleteView.as_view(), name='admin_period_delete'),
    path('admin/periods/<int:pk>/populate/', PopulateCandidatesView.as_view(), name='admin_period_populate'),
    path('admin/candidates/create/<int:period_id>/', CandidateCreateView.as_view(), name='admin_candidate_create'),
    path('admin/candidates/<int:pk>/update/', CandidateUpdateView.as_view(), name='admin_candidate_update'),
    path('admin/candidates/<int:pk>/delete/', CandidateDeleteView.as_view(), name='admin_candidate_delete'),
    path('admin/stats/', StatsView.as_view(), name='admin_stats'),
]
