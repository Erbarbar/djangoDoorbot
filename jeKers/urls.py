from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('b3', views.B3View.as_view(), name='b3'),
]
