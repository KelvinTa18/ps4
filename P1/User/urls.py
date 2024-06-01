from django.urls import path, include
from . import views
app_name = "User"
urlpatterns = [
    path('login/', views.login_def, name='login'),
    path('register/', views.register_def, name='register'),
    path('logout/', views.logout_def, name='logout'),
    # path('create/', views.create, name='create'),
    # path('update/<slug:id>', views.update, name='update'),
    # path('delete/', views.delete, name='delete'),
    # path('<slug:id>', views.viewDataDetail, name='viewDetail')
]
