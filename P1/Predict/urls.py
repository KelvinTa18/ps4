from django.urls import path, include
from . import views

app_name = "Predict"
urlpatterns = [
    path('', views.choose, name='choose'),
    path('<slug:id>', views.predictionOne, name='prediction-one'),
]
