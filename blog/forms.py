# https://docs.djangoproject.com/en/1.10/ref/forms/fields/
from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email_from = forms.EmailField()
    email_to = forms.EmailField()
    # The default widget can be overridden with the widget attribute.
    comments = forms.CharField(required=False, widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name','email','body')

class SearchForm(forms.Form):
    query = forms.CharField()
