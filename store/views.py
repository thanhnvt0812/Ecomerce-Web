from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django import forms
from django.db.models import Q
import json
from cart.cart import Cart
from payment.forms import ShippingForm
from payment.models import ShippingAddress
# Create your views here.
def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'home.html',{'products':products, 'categories':categories})

def about(request):
    return render(request, 'about.html',{})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            #do some shopping cart
            current_user = Profile.objects.get(user__id=request.user.id)
            #get their cart from db
            saved_cart = current_user.old_cart
            #convert db string to py dict
            if saved_cart:
                #convert to py dict using JSON
                converted_cart = json.loads(saved_cart)
                #add loaded cart to session
                #get the cart
                cart = Cart(request)
                #loop thru the cart and add the items from db
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)


            messages.success(request, "You have been logged in")
            return redirect('home')
        else:
            messages.success(request, "Error logging in!!! Please try again later")
            return redirect('login')
    else:
        return render(request, 'login.html',{})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
                # log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Your Account has been created - Please Fill Out Your Information Bellow!!!"))
            return redirect('update_info')
        else:
            messages.error(request, ("Whoops! There was a problem Registering, please try again..."))
            return redirect('register')
    else:
        return render(request, 'register.html', {'form': form})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id = request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance = current_user)

        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, "User has been updated successful")
            return redirect('home')
        return render(request,'update_user.html',{'user_form': user_form})
    else:
        messages.success(request, "You must login to access that page")
        return redirect('home')
    
def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
		# Did they fill out the form
        if request.method  == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
			# Is the form valid
            if form.is_valid():
                form.save()
                messages.success(request, "Your Password Has Been Updated...")
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, "update_password.html", {'form':form})
    else:
        messages.success(request, "You Must Be Logged In To View That Page...")
        return redirect('home')

def update_info(request):
	if request.user.is_authenticated:
		# Get Current User
		current_user = Profile.objects.get(user__id=request.user.id)
		# Get Current User's Shipping Info
		shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
		# Get original User Form
		form = UserInfoForm(request.POST or None, instance=current_user)
		# Get User's Shipping Form
		shipping_form = ShippingForm(request.POST or None, instance=shipping_user)		
		if form.is_valid() or shipping_form.is_valid():
			# Save original form
			form.save()
			# Save shipping form
			shipping_form.save()

			messages.success(request, "Your Info Has Been Updated!!")
			return redirect('home')
		return render(request, "update_info.html", {'form':form, 'shipping_form':shipping_form})
	else:
		messages.success(request, "You Must Be Logged In To Access That Page!!")
		return redirect('home')




def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})

def category(request, foo):
    #replace - with space
    foo = foo.replace('-', ' ')
    try:
        #look up category by name
        categories = Category.objects.all()
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'category':category, 'products':products, 'categories':categories})
    except:
        messages.success(request, "Category does not exist")
        return redirect('home')
    
def search(request):
    #if they fill the form
    if request.method == 'POST':
        searched = request.POST['searched']
        #query product in db model
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        #test for null
        if not searched:
            messages.success(request, "That product doesn't exist... Please try another")

        return render(request,'search.html',{'searched': searched})
    else:
        return render(request,'search.html',{})