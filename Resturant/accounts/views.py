from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from .forms import profileForm
from .models import Profile



# Create your views here.
def register (request):
    if request.method=='POST':
        fname=request.POST['first_name']
        lname=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password1=request.POST['password1']
        if password == password1:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'username is already register')
                return redirect ('register')
            try:
                validate_password(password)
                User.objects.create_user(first_name=fname,last_name=lname,username=username,email=email,password=password)
                messages.success(request,"Your account is successfully register.")
                return redirect('login')
            except ValidationError as e:
                for error in e.messages:
                    messages.error(request,error)
        
        else:
            messages.error(request,"password and confirm password doesnot match!!")
            return redirect('register')
    return render (request, 'accounts/register.html')

def log_in(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        remember_me=request.POST.get('remember_me')

        if not User.objects.filter(username=username).exists():
            messages.error(request, "this username is not register yet!!")
            return redirect('login')
    

        user=authenticate(username=username,password=password)


        if user is not None:
            login(request,user)

            if remember_me:
                request.session.set_expiry(12000000)
            else:
                request.session.set_expiry(0)

            next=request.POST.get('next','')
            return redirect(next if next else 'index')

        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            messages.error(request,"password invalid")
            return redirect ('login')
        
    next=request.GET.get('next','')

    return render (request,'accounts/login.html',{'next':next})

def log_out (request):
    logout(request)
    return redirect ('login')

@login_required (login_url='login')
def change_password(request):
    form=PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        form=PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect ('login')
    return render(request,'accounts/change_password.html', {'form':form})
@login_required (login_url='login')
def profile_dashboard(request):
    return render(request,'profile/dashboard.html')

@login_required (login_url='login')
def profile(request):
    profile,created=Profile.objects.get_or_create(user=request.user)
    form=profileForm(instance=profile)

    if request.method == 'POST':
        form=profileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    
    return render(request,'profile/profile.html',{'form':form,'profile':request.user.profile})
