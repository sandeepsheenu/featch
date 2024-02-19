# In parse/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('upload/', views.upload_documents, name='upload_documents'),
    path('document-list/', views.document_list, name='document_list'),
    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
