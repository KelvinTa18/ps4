from django.urls import path, include
from . import views

app_name = "Student"
urlpatterns = [
    path('', views.read, name='read'),
    path('create', views.create, name='create'),
    path('update/<slug:id>', views.update, name='update'),
    path('delete/<slug:id>', views.delete, name='delete'),
    path('predict/<slug:id>', views.predict, name='predict'),
    path('<slug:id>', views.readDetail, name='read-detail'),
]
