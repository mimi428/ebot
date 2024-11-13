from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.shop, name="shop"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
    path('categories/', views.categories, name="categories"),
    path('login/', views.login, name="login"),
    path('aboutus/', views.aboutus, name="aboutus"),
    path('contactus/', views.contactus, name="contactus"),
	path('update_item/', views.updateItem, name="update_item"),

	#for chatbot
    path('chatbot/', views.chatbot_view, name='chatbot'),
    path('chat/', views.chatbot_page, name='chatbot_page'),  # Page to interact with the chatbot


]

