from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("categories/<slug:category_slug>", views.index, name="list_by_tag"),
    path("auctions/<slug:auction>", views.detail, name="detail"),
    path("categories/", views.categories, name="categories"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("new-auction/", views.add_auction, name="new_auction"),
    path('add-to-watchlist', views.add_to_watchlist, name='add_to_watchlist'),
    path('remove-from-watchlist', views.remove_from_watchlist, name='remove_from_watchlist'),
    path('close-auction', views.close_auction, name='close_auction'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
]
