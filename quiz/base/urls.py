from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name = 'home'),
	path('game/<int:indice>', views.game, name = 'game'),
	path('end/', views.end, name = 'end')
]