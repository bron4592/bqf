from django.urls import path
from . import views
from . views import watchlistView
from structures import views as struc_views

urlpatterns = [
    path('', views.home, name='bqf-home'),
    path('search/', views.search, name='bqf-search'),
    path('watchlist/', views.watchlist, name='bqf-watchlist'),
    path('database/', struc_views.database, name='bqf-database'),
    path('trades/', views.trades, name='bqf-trades'),
    path('createWatchlist/', views.createWatch, name='bqf-createWatch'),
    path('hotlist/', views.hotlist, name='bqf-hotlist'),
    path('createhotlist/', views.createhotlist, name='bqf-createhotlist'),
    #path('watch/<int:pk>/', watchlistDetailView.as_view(), name='watch-detail'),
    ]
