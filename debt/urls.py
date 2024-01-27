from django.urls import path
from . import views
 

urlpatterns = [
    path('', views.home, name='home'),
    path('customer', views.newcustomer, name='customer'),
    path('analytics', views.analytics, name='analytics'),
    path('trends', views.trends, name='trends'),
    path('loan', views.loan, name='loan'),
    path('checkup', views.checkup, name='checkup'),
 

]
