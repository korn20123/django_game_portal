from django.urls import path
from . import views
urlpatterns= [
    path('', views.home, name='home'),
    path('add/', views.add, name='add'),
    path('delete/<int:game_id>', views.delete, name = 'delete'),
    path('play/<int:game_id>', views.play, name = 'play'),
    path('login/', views.login_view, name = 'login'),
    path('register/', views.register_view, name = 'register'),
    path('logout/', views.logout_view, name = 'logout'),
]