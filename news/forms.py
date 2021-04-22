from django import forms
from .models import News
from ckeditor.widgets import CKEditorWidget


class NewsBodyForm(forms.Form):
    news = forms.CharField(widget=CKEditorWidget())
