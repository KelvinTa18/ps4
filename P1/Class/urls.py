from django.urls import path, include
from . import views

app_name = "Class"
urlpatterns = [
    path('', views.read, name='read'),
    path('create', views.create, name='create'),
    path('update/<slug:id>', views.update, name='update'),
    path('delete/<slug:id>', views.delete, name='delete'),
    path('<slug:id>', views.readDetail, name='read-detail'),
]
