# https://docs.djangoproject.com/en/1.10/ref/forms/fields/
from django import forms

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email_from = forms.EmailField()
    email_to = forms.EmailField()
    # The default widget can be overridden with the widget attribute.
    comments = forms.CharField(required=False, widget=forms.Textarea)
