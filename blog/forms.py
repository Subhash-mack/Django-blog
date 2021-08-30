from django import forms
from django.forms import DateInput
from django.contrib.auth.models import User
from .models import Comments,Events

class CommentForm(forms.ModelForm):
    content=forms.CharField(label="Comment",widget=forms.Textarea(
        attrs={
            'class':'form-control',
            'placeholder':'Comment here !',
            'rows':4,
            'cols':50
        }
    ))
    class Meta:
        model=Comments
        fields=['content']

class EventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)

    class Meta:
        model=Events
        widgets = {
      'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M')
    }
        fields = ['title','start_time']