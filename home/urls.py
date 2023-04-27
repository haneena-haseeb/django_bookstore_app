from django.urls import path
from .import views

urlpatterns = [
    path('',views.tri,name="home"),
    path('sup/',views.signupage,name="sign"),
    path('log/',views.loginpage,name="login"),
    path('logout/',views.loginpage,name="logout"),
    path('menu/',views.menu,name="menu"),
    path('menu/<str:name>',views.menuview,name="menu"),
    path('menu/<str:cname>/<str:pname>',views.product_details,name="product_details"),
    path('addtocart',views.add_to_cart,name="addtocart"),
    path('cart',views.cart_page,name="cart"),
    path('remove_cart/<str:cid>',views.remove_cart,name="remove_cart"),
    path('addpro/',views.addproduct,name="pro"),
    path('pret/',views.pretrieve,name="pret"),
    path('pedit/<uid>',views.proupdate,name="proedit"),
    path('des/<uid>',views.destroy,name="destroy"),
   
]