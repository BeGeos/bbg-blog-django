from django import forms
from .models import Post
from ckeditor.widgets import CKEditorWidget


class PostBodyForm(forms.Form):
    post = forms.CharField(widget=CKEditorWidget())

