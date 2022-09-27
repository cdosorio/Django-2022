from ast import Try
from operator import truediv
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile, Skill, Message
from .forms import CustomUserCreationForm, MessageForm, ProfileForm, SkillForm
from .utils import paginateProfiles, searchProfiles

def loginUser(request):    
    if request.user.is_authenticated:
        return redirect('profiles')
    
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']
        
        try:            
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')
            
        user = authenticate(request, username=username, password = password)
        
        if user is not None:
            print('User logged in...')
            login(request, user)
            # ternary operator
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
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
            return redirect('edit-account')
        
        else:
            messages.error(request, 'Error ocurred during registration')
    
    context = {'page':page, 'form':form}
    return render(request, 'users/login_register.html', context)
        
def profiles(request):
    profiles, search_query = searchProfiles(request)    
    custom_range, profiles_page = paginateProfiles(request, profiles, 5)
        
    context = {'profiles_page': profiles_page, 'search_query':search_query, 'custom_range':custom_range}
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
    return render(request, 'users/account.html', context)

@login_required(login_url="login")
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
        
    context = {'form':form}
    return render(request, 'users/profile_form.html', context)


@login_required(login_url="login")
def createSkill(request):
    profile = request.user.profile 
    print('profile:' + str(profile))
    form = SkillForm()
    
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill was added')
            return redirect('account')
    
    context ={'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url="login")
def updateSkill(request, pk):
    print('updateSkill begin')
    # Check that only owner is updating skill
    profile = request.user.profile 
    skill = profile.skill_set.get(id=pk)    
    form = SkillForm(instance=skill)
    
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():      
            print('saving skill')      
            skill.save()
            messages.success(request, 'Skill was updated')
            return redirect('account')
    
    context ={'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url="login")
def deleteSkill(request, pk):
     # Only the owner can delete it 
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == "POST":
        skill.delete()
        messages.success(request, 'Skill was deleted')
        return redirect('account')
    
    context = {'object': skill}   
    return render(request, 'delete_template.html', context)


@login_required(login_url="login")
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequests': messageRequests, 'unreadCount':unreadCount} 
    return render(request, 'users/inbox.html', context)


@login_required(login_url="login")
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context ={'message':message}
    return render(request, 'users/message.html', context)


def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()
    
    try:
        sender = request.user.profile
    except:
        sender = None
        
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient
            
            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()
            
            messages.success(request, 'Your message was successfully sent')
            return redirect('user-profile', pk=recipient.id)        
    
    context ={'recipient':recipient , 'form':form}
    return render(request, 'users/message_form.html', context)