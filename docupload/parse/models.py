from django.db import models

# Create your models here.


class Document(models.Model):
    uploaded_file = models.FileField(upload_to='uploads/')
    text_content = models.TextField(blank=True)
    json_data = models.JSONField(blank=True)
