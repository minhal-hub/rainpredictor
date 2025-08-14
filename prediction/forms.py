from django import forms

class PredictionForm(forms.Form):
    location = forms.CharField(max_length=200, help_text='City or place name (e.g., Lahore)')
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
