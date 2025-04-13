from django import forms

from .models import Lead, Comment, LeadFile


class AddLeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ('company', 'first_name', 'last_name','phone', 'address', 'city', 'zipcode', 'country', 'email', 'description',
                  'priority', 'status', 'status_sale')


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

class AddFileForm(forms.ModelForm):
    class Meta:
        model = LeadFile
        fields = ('file',)
