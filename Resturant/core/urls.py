from django.urls import path
from.views import about, index,contact,menu,services,cart
urlpatterns=[
    path("",index, name="index"),
    path("about/",about, name='about'),
    path("contact/",contact, name='contact'),
    path("menu/",menu, name="menu"),
    path("services/",services, name="services"),
    path("cart/",cart, name="cart")


]