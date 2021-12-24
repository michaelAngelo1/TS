from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'), 
    path('report/', views.report, name='report'),
    path('listdeposit/', views.DepositListView.as_view, name='deposit-list'),
]
