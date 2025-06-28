from django import forms

from .models import Client, Comment, ClientFile


class AddClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('first_name', 'last_name','phone', 'address', 'city', 'country', 'zipcode', 'email',
                  'description', 'company', 'status', 'website',)


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)


class AddFileForm(forms.ModelForm):
    class Meta:
        model = ClientFile
        fields = ('file',)
