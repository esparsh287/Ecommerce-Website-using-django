from django.shortcuts import redirect, render
from .models import Category, Product
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm



def home(request):
  products=Product.objects.all()
  return render(request, 'home.html',{'products':products})


def about(request):
  return render(request, 'about.html')


def login_user(request):
  if request.method=="POST":
    username=request.POST['username']
    password=request.POST['password']
    user= authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user)
      messages.success(request, ("You have been logged in !!!"))
      return redirect('home')

    else:
      messages.error(request, ("Please Enter Correct Credentials"))
      return redirect('login')
  return render(request, 'login.html', {})


def logout_user(request):
  logout(request)
  messages.success(request, ("You have been logged out!!!"))
  return redirect('login')



def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "You have registered successfully!!!")
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SignUpForm()

    return render(request, 'register.html', {'form': form})



def product(request, pk):
   product=Product.objects.get(id=pk)
   return render(request, 'product.html',{'product':product})


def category(request, cat):
   cat= cat.replace('-', ' ')
   try:
      category= Category.objects.get(name=cat)
      products= Product.objects.filter(category=category)
      return render(request, 'category.html', {'products':products, 'category':category})
   except:
      messages.success("The Category doesn't exist!!!")
      return redirect('home')
      
   
