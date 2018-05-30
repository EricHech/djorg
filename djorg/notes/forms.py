from django import forms
from .models import Note


class NotesForm(forms.ModelForm):

    class Meta:  # Meta != monkey
        model = Note
        fields = ('title', 'content')
