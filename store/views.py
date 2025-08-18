from django.shortcuts import redirect, render
from .models import Category, Product, Profile
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django.contrib.auth.models import User
import json
from cart.cart import Cart


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
      current_user= Profile.objects.get(user__id=request.user.id)
      saved_cart= current_user.old_cart
      if saved_cart:
         converted_cart=json.loads(saved_cart)
         cart=Cart(request)
         for key,value in converted_cart.items():
            cart.db_add(product=key, quantity=value)
         
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
            messages.success(request, "Username Created successfully!!! Please complete the details")
            return redirect('update_info')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SignUpForm()

    return render(request, 'register.html', {'form': form})



def product(request, pk):
   product=Product.objects.get(id=pk)
   return render(request, 'product.html',{'product':product})


def category(request, foo):
   foo= foo.replace('-', ' ')
   try:
      category= Category.objects.get(name=foo)
      products= Product.objects.filter(category=category)
      return render(request, 'category.html', {'products':products, 'category':category})
   except:
      messages.success("The Category doesn't exist!!!")
      return redirect('home')
   



def category_summary(request):
   categories= Category.objects.all()
   return render(request, 'category_summary.html', {"categories": categories})



def update_user(request):
   if request.user.is_authenticated:
        current_user=User.objects.get(id=request.user.id)
        form= UpdateUserForm(request.POST or None, instance=current_user) #instance gives the info of current user
        if form.is_valid():
          form.save()
          login(request, current_user)
          messages.success(request,"Profile Updated successfully!!!!")
          return redirect('home')
        return render(request, 'update_user.html',{'form':form})
   else:
      messages.error(request,"Ypu must be logged in!!!")
      return redirect('home')
   

def update_password(request):
   if request.user.is_authenticated():
      current_user=request.User
      if request.method=="POST":
         form=ChangePasswordForm(current_user, request.POST)
         if form.is_valid():
            form.save()
            messages.success(request,"Password Changed Sucessfully!!!")
            return redirect('update_user')
         else:
            messages.error(request, "Error in changing Password!!")
            return redirect("update_password")
      else:
         form= ChangePasswordForm(current_user)
         return redirect('update_password.html',{'form':form})
   else:
      messages.error(request,"You must be logged in!!!!")
      return redirect('home')
   


def update_info(request):
   if request.user.is_authenticated:
        current_user=Profile.objects.get(user__id=request.user.id)
        form= UserInfoForm(request.POST or None, instance=current_user) #instance gives the info of current user
        if form.is_valid():
          form.save()
          
          messages.success(request,"Your Info has been Updated!!!!")
          return redirect('home')
        return render(request, 'update_info.html',{'form':form})
   else:
      messages.error(request,"You must be logged in!!!")
      return redirect('home')
   

def search(request):
   if request.method=="POST":
      searched= request.POST['searched']
      searched=Product.objects.filter(name__icontains=searched)
      if not searched:
         messages.error(request, "Product does not exist!!!!")
         return render(request, 'search.html', {})
      return render(request, 'search.html', {'searched':searched})
   else:
      return render(request, 'search.html', {})
   
   
    
      
   
