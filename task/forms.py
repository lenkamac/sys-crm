from django import forms

from client.models import Client
from lead.models import Lead
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'lead', 'client', 'assigned_to','due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
            'lead': forms.Select(attrs={'class': 'form-select'}),
            'client': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        lead = cleaned_data.get('lead')
        client = cleaned_data.get('client')

        # Ensure not both lead and client are selected
        if lead and client:
            raise forms.ValidationError(
                "A task cannot be related to both a lead and a client simultaneously."
            )

        return cleaned_data
