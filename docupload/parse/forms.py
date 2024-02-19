# In parse/forms.py
from django import forms
from .models import Document
from multiupload.fields import MultiFileField

class DocumentForm(forms.ModelForm):
    uploaded_files = MultiFileField(min_num=1, max_num=10, max_file_size=1024*1024*5)  # Max size is 5 MB
    class Meta:
        model = Document
        fields = ['uploaded_files']
