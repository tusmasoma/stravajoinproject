
from django.urls import path
from . import views

app_name='stravajoin'

urlpatterns = [
    path('',views.index_view,name='index'),
    path('join/',views.join_view,name='join')
]
