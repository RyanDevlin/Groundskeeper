from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
	path('', views.dash_index, name='dash_index'),
	path("<int:pk>/", views.plant_detail, name="plant_detail"),
	path('<str:gname>/', views.plant_add, name="new"),
	path('<int:pk>/delete/', views.plant_delete, name='delete'),
	path('<int:pk>/water/', views.plant_water, name='water'),
	path('<int:pk>/settings/', views.settings_page, name='settings_page'),
	path('<int:gpk>/plant/<int:ppk>/settings/', views.plant_settings, name='plant_settings'),
]