from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('create_project/', views.create_project, name="create_project"),
    path('projects/', views.projects, name="projects"),
    path('delete_project/<str:pk>/', views.delete_project, name="delete_project"),
    path('select_project/<str:pk>/', views.select_project, name="select_project"),
    path('articles/', views.articles, name="articles"),
    path('upload_batch/<str:pk>/', views.upload_batch, name="upload_batch"),
    path('specific_article', views.specific_article, name="specific_article"),

    path('review_logs', views.logs_review, name="review_logs"),

]
