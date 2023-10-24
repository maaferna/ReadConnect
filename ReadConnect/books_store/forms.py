# forms.py
from django import forms

class BookStatusForm(forms.Form):
    currently_reading = forms.BooleanField(required=False)
    want_to_read = forms.BooleanField(required=False)
