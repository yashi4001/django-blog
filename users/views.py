from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required



def register(request):
    if request.method=='POST':
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            form.save() #saving user to db
            username=form.cleaned_data.get('username')
            messages.success(request,f'Account created for {username}')
            return redirect('user-login')
    else:
        form=UserRegisterForm()
    return render(request,"users/register.html",{'form':form})

@login_required
def profile(request):
    if request.method =='POST':
        u_form=UserUpdateForm(request.POST,instance=request.user)
        p_form=ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f'Profile updated!')
            return redirect('user-profile')

    else:        
        u_form=UserUpdateForm(instance=request.user)
        p_form=ProfileUpdateForm(instance=request.user.profile)
    context={
        'uform':u_form,
        'pform':p_form
    }
    return render(request,"users/profile.html",context)

# Create your views here.
