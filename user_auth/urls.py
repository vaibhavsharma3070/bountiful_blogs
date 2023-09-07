from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_process, name="login"),
    path('register/', views.register_process, name="register"),
    path('logout/', views.logout_process, name="logout"),
]
