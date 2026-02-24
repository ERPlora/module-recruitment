from django import forms
from django.utils.translation import gettext_lazy as _

from .models import JobPosition, Candidate

class JobPositionForm(forms.ModelForm):
    class Meta:
        model = JobPosition
        fields = ['title', 'department', 'description', 'status', 'vacancies', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'department': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'description': forms.Textarea(attrs={'class': 'textarea textarea-sm w-full', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'select select-sm w-full'}),
            'vacancies': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'toggle'}),
        }

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['position', 'name', 'email', 'phone', 'stage', 'resume_notes', 'rating']
        widgets = {
            'position': forms.Select(attrs={'class': 'select select-sm w-full'}),
            'name': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'email': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'email'}),
            'phone': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'stage': forms.Select(attrs={'class': 'select select-sm w-full'}),
            'resume_notes': forms.Textarea(attrs={'class': 'textarea textarea-sm w-full', 'rows': 3}),
            'rating': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
        }

