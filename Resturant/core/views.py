from django.shortcuts import render, redirect
from .models import Contact
from django.contrib import messages
from django.core.mail import send_mail
from datetime import datetime
from.models import Category,Momo
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    category=Category.objects.all()
    cateid=request.GET.get('category')#1
    if cateid:
        momo=Momo.objects.filter(category=cateid)
    else:
        momo=Momo.objects.all()
    if request.method =='POST':
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        message=request.POST['message']

        Contact.objects.create(name=name,email=email,phone=phone,message=message)
        subject="django tarining"
        message="Thanks For Filling Form"
        from_email="jsscraut@gmail.com"
        recipient_list=[email]
        send_mail(subject,message,from_email,recipient_list,fail_silently=False)

        messages.success(request,"Your form is successfully submit and please check your email!")
        return redirect('index')
    
    context={
        'date':datetime.now(),
        'category':category,
        'momo':momo
    }
     
    return render(request,'core/index.html',context)

@login_required(login_url='login')
def about(request):
    return render(request,'core/about.html')

def contact(request):
    return render(request,'core/contact.html')

@login_required(login_url='login')
def menu(request):
    return render(request,'core/menu.html')

def services(request):
    return render(request,'core/services.html')