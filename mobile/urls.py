from django.urls import path, include
from mobile import views

urlpatterns = [
    path("catagory_list/", views.catagory_list, name="catagory_list"),
    path("store/", views.store, name="store"),
    path("product_list/", views.product_list, name="product_list"),
    path("product/<int:id>/", views.product_detail, name="product_detail"),
]