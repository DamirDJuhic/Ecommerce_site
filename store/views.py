from imp import reload
import re
from django import template
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
import datetime
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

from django.views.decorators.csrf import csrf_exempt
from .models import *
from .utils import cookieCart, cartData,guestOrder
def store(request):
	data = cookieCart(request)
	cartItems = data['cartItems']
		

	products = Product.objects.all()
	context = {"products":products,'cartItems':cartItems}
	return render(request, 'store/store.html', context)

def cart(request):

	data = cookieCart(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items,'order':order,'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):

	data = cookieCart(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items,'order':order,'cartItems':cartItems,}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']

	print('Action :', action)
	print('productId :', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)
	
	orderItem, created = OrderItem.objects.get_or_create(order=order,product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()
	
	if orderItem.quantity <= 0:
		orderItem.delete()
	return JsonResponse('item was added',safe=False)
	
#from django.views.decorators.csrf import csrf_exempt
#@csrf_exempt

def processOrder(request):
	transaction_id=datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer=request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		total = float(data['form']['total'])
		order.transaction_id = transaction_id

		if total == order.get_cart_total:
			order.complete = True
		order.save()

	else:
		customer,order = guestOrder(request,data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == float(order.get_cart_total):
			order.complete = True
	order.save()

	if order.shipping==True:
		ShippingAddress.objects.create(
			customer=customer,
			order=order,
			address= data['shipping']['address'],
			city= data['shipping']['city'],
			state= data['shipping']['state'],
			zipcode= data['shipping']['zipcode'],
			number= data['shipping']['number'],
		)

	return JsonResponse('Payment complete',safe=False)

def waypaying(request):
	data = cookieCart(request)
	cartItems = data['cartItems']

	context = {'cartItems':cartItems}
	return render(request,"store/waypaying.html",context)

def wayshipping(request):
	data = cookieCart(request)
	cartItems = data['cartItems']
	

	context = {'cartItems':cartItems}
	return render(request,"store/wayshipping.html",context)

def complaint(request):
	data = cookieCart(request)
	cartItems = data['cartItems']

	context = {'cartItems':cartItems}
	return render(request,"store/complaint.html",context)

def contact(request):
	data = cookieCart(request)
	cartItems = data['cartItems']

	if request.method=="POST":
		contact= Contact()
		name = request.POST.get('name')
		email = request.POST.get('email')
		subject = request.POST.get('subject')
		contact.name=name
		contact.email=email
		contact.subject=subject
		contact.save()
		return render(request,"store/contact.html")
	context = {'cartItems':cartItems}
	return render(request,"store/contact.html",context)

def aboutus(request):
	data = cookieCart(request)
	cartItems = data['cartItems']

	context = {'cartItems':cartItems}
	return render(request,"store/aboutus.html",context)

def showslides(request):
	return render(request,'store.html')

