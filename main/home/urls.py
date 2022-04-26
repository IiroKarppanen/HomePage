from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('<int:item_id>/delete_shortcut/', views.delete_shortcut, name='delete_shortcut'),
    path('<str:background_id>/change_background/', views.change_background, name='change-background'),
]