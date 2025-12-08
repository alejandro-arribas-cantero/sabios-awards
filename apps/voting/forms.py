from django import forms
from .models import VotingPeriod, Candidate

class VotingPeriodForm(forms.ModelForm):
    MONTH_CHOICES = [
        (1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'),
        (5, 'Mayo'), (6, 'Junio'), (7, 'Julio'), (8, 'Agosto'),
        (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')
    ]
    
    month = forms.TypedChoiceField(
        choices=MONTH_CHOICES, 
        widget=forms.Select(attrs={'class': 'form-select'}),
        coerce=int,
        label="Mes"
    )

    class Meta:
        model = VotingPeriod
        fields = ['month', 'year', 'status', 'winner_photo', 'manual_winner']
        widgets = {
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'winner_photo': forms.FileInput(attrs={'class': 'form-control'}),
            'manual_winner': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['manual_winner'].queryset = Candidate.objects.filter(period=self.instance)
        else:
            self.fields['manual_winner'].queryset = Candidate.objects.none()

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['period', 'name', 'photo', 'photo_winner', 'nomination_reason']
        widgets = {
            'period': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'photo_winner': forms.FileInput(attrs={'class': 'form-control'}),
            'nomination_reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
