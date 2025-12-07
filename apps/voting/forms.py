from django import forms
from .models import VotingPeriod, Candidate

class VotingPeriodForm(forms.ModelForm):
    class Meta:
        model = VotingPeriod
        fields = ['month', 'year', 'status', 'winner_photo']
        widgets = {
            'month': forms.NumberInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'winner_photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['period', 'name', 'photo']
        widgets = {
            'period': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }
