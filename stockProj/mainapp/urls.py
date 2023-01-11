from django.urls import path,include
from .import views

urlpatterns = [
    
    path('', views.register, name='Register'),
    path('home/', views.stockPicker, name='stockpicker' ),
    path('stocktracker/', views.stockTracker, name='stocktracker' ),
]