from django import forms

from .models import Task, TaskComment


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'lead', 'client', 'assigned_to','due_date', 'due_time']
        widgets = {
            'due_date':forms.DateField(required=False),
            'due_time':forms.TimeField(required=False),
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
        due_date = cleaned_data.get("due_date")
        due_time = cleaned_data.get("due_time")
        if due_date and due_time:
            # Combine to datetime if both provided (optional, as per your app logic)
            import datetime
            cleaned_data['due_datetime'] = datetime.datetime.combine(due_date, due_time)

        # Ensure not both lead and client are selected
        if lead and client:
            raise forms.ValidationError(
                "A task cannot be related to both a lead and a client simultaneously."
            )

        return cleaned_data


class TaskCommentForm(forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}),
        }


class TaskEditForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'status', 'priority', 'assigned_to' ]
        widgets = {
            'due_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
        }
