from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="shop"),
    path("<str:category>/", menu_category, name="shop-category"),
    path("add-to-cart/<pk>/", add_to_cart, name="add-to-cart"),
    path("remove-from-cart/<pk>/", remove_from_cart, name="remove-from-cart"),
]
