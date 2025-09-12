from django.shortcuts import render, redirect
from .models import Contact
from django.contrib import messages
from django.core.mail import send_mail
from datetime import datetime
from.models import Category,Momo
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    category = Category.objects.all()
    cateid = request.GET.get('category')  # Get selected category

    if cateid:
        momo = Momo.objects.filter(category=cateid)
        selected_category = int(cateid)  # Pass to template
    else:
        momo = Momo.objects.all()
        selected_category = None  # No category selected
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
        'momo':momo,
         'selected_category': selected_category 
    }
     
    return render(request,'core/index.html',context)

# @login_required(login_url='login')
def about(request):
    return render(request,'core/about.html')

def contact(request):
    return render(request,'core/contact.html')

@login_required(login_url='login')
def menu(request):
    category = Category.objects.all()             # get all categories
    cateid = request.GET.get('category')          # get selected category from URL

    if cateid:
        momo = Momo.objects.filter(category=cateid)  # filter momos by category
        selected_category = int(cateid)
    else:
        momo = Momo.objects.all()                    # show all momos if no category
        selected_category = None

    context = {
        'category': category,
        'momo': momo,
        'selected_category': selected_category,
    }
    return render(request, 'core/menu.html', context)


def services(request):
    return render(request,'core/services.html')

def cart(request):
    return render(request,'core/cart.html')

def index(request):
    category = Category.objects.all()
    cateid = request.GET.get('category')

    if cateid:
        momo = Momo.objects.filter(category=cateid)
        current_category = int(cateid)  # use the same name as template
    else:
        momo = Momo.objects.all()
        current_category = None

    context = {
        'date': datetime.now(),
        'category': category,
        'momo': momo,
        'current_category': current_category,  # 🔑 match template
    }
    return render(request, 'core/index.html', context)