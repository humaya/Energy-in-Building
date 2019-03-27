from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('methodology', views.methodology, name='methodology'),
    path('results', views.results, name='results'),
    path('upload-csv', views.upload_file, name='upload-csv'),
]
