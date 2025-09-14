from django.urls import path
from . import views
from .views import about, index, contact, menu, services, cart, add_to_cart, increase_quantity, decrease_quantity, remove_from_cart
urlpatterns=[
    path("",index, name="index"),
    path("about/",about, name='about'),
    path("contact/",contact, name='contact'),
    path("menu/",menu, name="menu"),
    path("services/",services, name="services"),
    path("cart/",cart, name="cart"),

      # Cart actions
    path("cart/add/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path("cart/increase/<int:item_id>/", increase_quantity, name="increase_quantity"),
    path("cart/decrease/<int:item_id>/", decrease_quantity, name="decrease_quantity"),
    path("cart/remove/<int:item_id>/", remove_from_cart, name="remove_from_cart"),
    path("place-order/", views.place_order, name="place_order"),


]