from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import *
from django.contrib import messages
import json
# Create your views here.


def tri(request):
    return render(request,"trial.html")

def signupage(request):
    if request.method=="POST":
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            messages.warning(request,"Password doesnt match")
            return render(request,'signup.html')
        try:
            if User.objects.get(username=uname):
                return HttpResponse('user name already exist!')

        except Exception as identifier:
            pass
        my_user=User.objects.create_user(uname,email,pass1)
        my_user.save()
        return render(request,'login.html')
    return render(request,"signup.html")

def loginpage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            messages.warning(request,"Login Success")
            return redirect('home')
        else:
            messages.warning(request,"Invalid User")
            return redirect('login')
        # print(username,pass1)
    return render(request,"login.html")

def logoutpage(request):
    logout(request)
    messages.info(request,"logout success")
    return redirect('login')

def menu(request):
    category=Category.objects.filter(status=0)
    return render(request,"menu.html",{"category":category})

def menuview(request,name):
    if(Category.objects.filter(name=name,status=0)):
        products=Product.objects.filter(category__name=name)
        return render(request,'products/index.html',{"products":products,"category":name})
    else:
        messages.warning(request,"No such Category Found")
        return redirect('menu')

def product_details(request,cname,pname):
    if(Category.objects.filter(name=cname,status=0)):
        if(Product.objects.filter(name=pname,status=0)):
            products=Product.objects.filter(name=pname,status=0).first()
            return render(request,'products/product_details.html',{"products":products})
        else:
            messages.error(request,"No such Product Found")
            return redirect('menu')
    else:
        messages.error(request,"No such Category Found")
        return redirect('menu')

def cart_page(request):
  if request.user.is_authenticated:
    cart=Cart.objects.filter(user=request.user)
    return render(request,"cart.html",{"cart":cart})
  else:
    return redirect("/")

def remove_cart(request,cid):
  cartitem=Cart.objects.get(id=cid)
  cartitem.delete()
  return redirect("/cart")

def add_to_cart(request):
   if request.headers.get('x-requested-with')=='XMLHttpRequest':
    if request.user.is_authenticated:
      data=json.load(request)
      product_qty=data['product_qty']
      product_id=data['pid']
      #print(request.user.id)
      product_status=Product.objects.get(id=product_id)
      if product_status:
        if Cart.objects.filter(user=request.user.id,product_id=product_id):
          return JsonResponse({'status':'Product Already in Cart'}, status=200)
        else:
          if product_status.quantity>=product_qty:
            Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
            return JsonResponse({'status':'Product Added to Cart'}, status=200)
          else:
            return JsonResponse({'status':'Product Stock Not Available'}, status=200)
    else:
      return JsonResponse({'status':'Login to Add Cart'}, status=200)
   else:
    return JsonResponse({'status':'Invalid Access'}, status=200)


def addproduct(request):
    if request.method=="GET":
        return render(request,"product.html")
    elif request.method=="POST":
        c=request.POST['ven']
        c=request.POST['ven']
        n=request.POST['name']
        q=request.POST['qty']
        o=request.POST['oprice']
        p=request.POST['price']
        d=request.POST['desc']
        a=Product.objects.create(category=v,vendor=c,name=n,quantity=q,original_price=o,selling_price=p,description=d)
        return redirect('pret')

def pretrieve(request):
    pro=Product.objects.all()
    context={}
    context['data']=pro
    return render(request,"pro_retrieve.html",context)  

def proupdate(request,uid):
    if request.method=="GET":
        pro=Product.objects.get(id=uid)
        context={}
        context['data']=pro
        return render(request,"pro_edit.html",context)
    elif request.method=="POST":
        c=request.POST['ven']
        n=request.POST['name']
        p=request.POST['price']
        a=Product.objects.filter(id=uid).update(vendor=c,name=n,selling_price=p)
        return redirect('pret')

def destroy(request,uid):
    a=Product.objects.filter(id=uid).delete()
    return redirect('pret')

