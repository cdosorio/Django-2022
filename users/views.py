from ast import Try
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import CustomUserCreationForm

def loginUser(request):    
    if request.user.is_authenticated:
        return redirect('profiles')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:            
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')
            
        user = authenticate(request, username=username, password = password)
        
        if user is not None:
            print('User logged in...')
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, 'Username OR password is wrong')
            
    return render(request, 'users/login_register.html')

def logoutUser(request):
    logout(request) # deletes the session
    messages.info(request, 'Username logged out')
    return redirect('login')

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'User created')
            
            login(request, user)
            return redirect('profiles')
        
        else:
            messages.error(request, 'Error ocurred during registration')
    
    context = {'page':page, 'form':form}
    return render(request, 'users/login_register.html', context)
        
def profiles(request):
    profiles = Profile.objects.all()
    context = {'profiles': profiles}
    return render(request, 'users/profiles.html', context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    
    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description__exact="")
    
    context = {'profile': profile, 'topSkills': topSkills, 'otherSkills': otherSkills}
    return render(request, 'users/user-profile.html', context)

@login_required(login_url="login")
def userAccount(request):
    profile = request.user.profile
    
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
        
    context = {'profile': profile, 'skills': skills, 'projects':projects}
    return render(request, 'users/user-account.html', context)