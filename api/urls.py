from django.urls import path
from . import views


urlpatterns = [
	path('', views.apiOverview, name="api-overview"),
	path('reg-list/', views.regList, name="reg-list"),
	path('reg-detail/<str:pk>/', views.regDetail, name="reg-detail"),
	path('reg-create/', views.regCreate, name="reg-create"),

	path('reg-update/<str:pk>/', views.regUpdate, name="reg-update"),
	path('reg-delete/<str:pk>/', views.regDelete, name="reg-delete"),
]
