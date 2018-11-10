from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('stock/', views.stock, name='stock'),
    path('import_portfolio/', views.import_portfolio, name='import_portfolio')
]
