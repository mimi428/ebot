from django.shortcuts import render
from django.http import JsonResponse
from .models import *
import json

def shop(request):

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		#Create empty cart for now for non-logged in user
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0}
		cartItems = order['get_cart_items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'shop/shop.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        # Create empty cart for non-logged-in user
        items = [] 
        # Create an empty order-like object for non-authenticated users
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order.get_cart_items

    # Make sure the order is defined in all cases
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    
    # Ensure a valid HttpResponse is returned
    return render(request, 'shop/cart.html', context)

def checkout(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all(); cartItems = order.get_cart_items
	else:
		#Create empty cart for now for non-logged in user
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0}; cartItems = order ['get_cart_items']

	context = {'items':items, 'order':order, 'cartItems': cartItems}
	return render(request, 'shop/checkout.html', context)


def categories(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all(); cartItems = order.get_cart_items
    else:
		#Create empty cart for now for non-logged in user
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}; cartItems = order ['get_cart_items']
    categorys = Category.objects.all()
    context = {'categorys':categorys, 'cartItems':cartItems}
    return render(request,'shop/categories.html',context)


def login(request):
    context={}
    return render(request,'shop/login.html',context)

def aboutus(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all(); cartItems = order.get_cart_items
    else:
		#Create empty cart for now for non-logged in user
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}; cartItems = order ['get_cart_items']
    categorys = Category.objects.all()
    context = {'categorys':categorys, 'cartItems':cartItems}
    return render(request,'shop/aboutus.html',context)

def contactus(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all(); cartItems = order.get_cart_items
    else:
		#Create empty cart for now for non-logged in user
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}; cartItems = order ['get_cart_items']
    categorys = Category.objects.all()
    context = {'categorys':categorys, 'cartItems':cartItems}
    return render(request,'shop/contactus.html',context)

def updateItem(request):
     data= json.loads(request.body)
     productId= data['productId']
     action= data['action']
     print('Action:',action)
     print('ProductId:',productId)

     customer = request.user.customer
     product = Product.objects.get(id=productId)
     order, created = Order.objects.get_or_create(customer=customer, complete=False)

     orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

     if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
     elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

     orderItem.save()

     if orderItem.quantity <= 0:
        orderItem.delete()


     return JsonResponse('Item was added', safe=False)

# for the chatbot


from .naive_bayes_chatbot import generate_response  # Import your chatbot function

def chatbot_view(request):
    user_message = request.GET.get('message', '')  # Capture the user’s message from a GET request
    if user_message:
        bot_response = generate_response(user_message)  # Generate chatbot response
    else:
        bot_response = "ramrari bol"

    return JsonResponse({'response': bot_response})  # Return JSON response to the frontend


def chatbot_page(request):
    context={}
    return render(request, 'shop/chatbot.html',context)