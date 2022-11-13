from django.urls import path
from django.views.generic import TemplateView
from . import views


urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('wayshipping/', views.wayshipping, name="wayshipping",),
	path('waypaying/', views.waypaying, name="waypaying"),
	path('complaint/', views.complaint, name="complaint"),
	path('contact/', views.contact, name="contact"),
	path('aboutus/', views.aboutus, name="aboutus"),

	path('email_template/', views.processOrder, name="email_template"),
	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
	path('',views.showslides),
]