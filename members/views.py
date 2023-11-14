
from django.shortcuts import render, redirect
from pytz import timezone
from api.models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count, Sum, F
from django.db.models.functions import TruncMonth
from django.db import connection
from sacco.functions import dictfetchall
from datetime import datetime, timedelta, time, date
import datetime
from django.contrib.auth.models import Group
from sacco.forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from sacco.decorators import *
import calendar
from sacco.functions import *
import decimal
from django.utils.timezone import make_aware
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from random import randint
from django.core.cache import cache
from sacco.celery import *
from django.db.models import Q
from sacco.constants import *
from django.core.paginator import Paginator
from openpyxl import Workbook
from django.http import HttpResponse
from django.db import connection



""" Add Member """
@login_required(login_url='sign-in')
def members(request):
    members = User.objects.filter(is_superuser=0, is_staff=0).select_related('userprofile').values('id', 'first_name', 'last_name', 'username', 'userprofile__member_no_shares', 'userprofile__member_no_savings', 'userprofile__id_no')

    page_obj = members
    #paginator = Paginator(members, 10)
    #page_number = request.GET.get('page')
    #page_obj = Paginator.get_page(paginator, page_number)

    context = {'members': members, 'page_obj': page_obj }
    return render(request, 'sacco/members/members.html', context)

@login_required(login_url='sign-in')
def add_member(request):
    form = CreateUserForm()
    user_profile = UserProfileForm()
    groups = Group.objects.get(name='Member')
    values = request.POST
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        
        username = request.POST['username']
        member_no_shares = request.POST['member_no_shares']
        member_no_savings = request.POST['member_no_savings']
        id_no = request.POST['id_no']
        
        is_active = request.POST.get('is_active')
        
        print(is_active)
       
        print('Printing POST:', request.POST)
        print('Printing Errors:', form.errors )
        if num_length(username) != PHONE_NUMBER:
            messages.error(request, "Phone number number must have " + str(PHONE_NUMBER) + ' digits')    
        elif(starts_with_zero(username) == False):       
            messages.error(request, "Phone number number must begin with 0")   
        elif not (member_no_shares) and (member_no_savings):
            messages.error(request, "Member Number is required")
        elif(UserProfile.objects.filter(member_no_shares=member_no_shares, member_no_savings=member_no_savings)):
            messages.error(request, "Member Number Exists") 
        else:
            if form.is_valid():
               
                user = form.save(commit=False)
                user.email = f'user{randint(1, 99999)}@wauminisacco.co.ke'
                user.password = User.objects.make_random_password()
                user.is_active = is_active
                user.save()
                user = User.objects.get(pk=user.id) 
                
               
             
                user_profile_form = UserProfileForm(request.POST, instance=user.userprofile)
                if user_profile_form.is_valid():

                    if not id_no:
                        id_no = None
                        
                    if not member_no_shares:
                        member_no_shares = None
                        
                    if not member_no_savings:
                        member_no_savings = None


                    profile = user_profile_form.save(commit=False)
                    profile.save()
                    

                

                username = form.cleaned_data.get('username')    
                g = form.cleaned_data.get('group')
            
                print('selected user role:',g)
                
                group = Group.objects.get(id=g)
                # Add user to group
                user.groups.add(group)
            
                    
                cache.clear()
                messages.success(request,  username + " has been created successfully")
                
                return redirect('members')
    else:
        
        form = CreateUserForm()

    
    context = {'groups': groups, 'form': form, 'values' : values, 'user_profile' : user_profile }

    if groups:
        return render(request, 'sacco/members/add-member.html', context)
    else:
        messages.error(request,  "Error! Roles are not added, Please contact system administrator")
        return render(request, 'sacco/error.html', context)

@login_required(login_url='sign-in')
def edit_member(request, id):
    # Check if user exists
    groups = Group.objects.get(name='Member')
    try:
        user = User.objects.get(pk=id)

    except User.DoesNotExist:
        messages.error(request, ERROR_404)
        return render(request, 'sacco/error.html')

    #user_profile = UserProfileForm(request.POST, instance=user.userprofile)
    try:
        user_profile = UserProfileForm(request.POST, instance=user.userprofile)
    

        context = {
            'groups': groups, 
            'values': user,
            'user_profile' : user_profile,
            }
        

        print(request.POST)
        if request.method == 'GET':
            return render(request, 'sacco/members/edit-member.html', context)

        if request.method == 'POST':
            e = request.POST['email']
            u = request.POST['username']

            member_no_shares = request.POST['member_no_shares']
            member_no_savings = request.POST['member_no_savings']

            id_no = request.POST['id_no']
            is_active = request.POST['is_active']


            if not is_active:
                messages.error(request, "Is Member is required")
                return render(request, 'sacco/members/edit-member.html', context)

            if User.objects.exclude(pk=id).filter(email=e):
                messages.error(request, MEMBER_EMAIL_EXISTS)
                return render(request, 'sacco/members/edit-member.html', context)

            if User.objects.exclude(pk=id).filter(username=u):
                messages.error(request, "Phone number already exists")
            elif(num_length(u) != PHONE_NUMBER):
                messages.error(request, "Phone number number must have " + str(PHONE_NUMBER) + ' digits starting with 0') 
            elif(starts_with_zero(u) == False):       
                messages.error(request, "Phone number number must begin with 0")  
            elif(UserProfile.objects.filter(member_no_savings=member_no_savings)).exclude(user_id=id):
                messages.error(request, "Member Number Savings Exists")
            elif(UserProfile.objects.filter(member_no_shares=member_no_shares)).exclude(user_id=id):
                messages.error(request, "Member Number Shares Exists")
            elif(UserProfile.objects.filter(id_no=id_no)).exclude(user_id=id):
                messages.error(request, "ID Number Exists")
            else:
                # Get user information from form
                user.username = request.POST['username']
                user.first_name = request.POST['first_name']
                user.last_name = request.POST['last_name']
                user.email = f'user{randint(1, 99999)}@wauminisacco.co.ke'
                # user.password = User.objects.make_random_password()
                user.is_active = is_active

                # Save user
                user.save()
                # Remove user from group           
                user.groups.set([])
                
                g  = request.POST['group']
                group = Group.objects.get(id=g)
                # Add user to group
                user.groups.add(group)

                print('selected user role:',g)
                
                user_profile_form = UserProfileForm(request.POST, instance=user.userprofile)
                if user_profile_form.is_valid():

                    if not id_no:
                        id_no = None
                    else:
                        user_profile_form.id_no = id_no
                        
                    if not member_no_shares:
                        member_no_shares = None
                    else:
                        user_profile_form.member_no_shares = member_no_shares
                        
                    if not member_no_savings:
                        member_no_savings = None
                    else:
                        user_profile_form.member_no_savings = member_no_savings
                    
                    profile = user_profile_form.save(commit=False)
                    profile.save()

                else:
                    messages.error(request, "User profile form is not valid" + str(user_profile_form.errors))
            
                
                cache.clear()
                messages.success(request,  user.username + " has been updated successfully")
                return redirect('members')

        return render(request, 'sacco/members/edit-member.html', context)
    
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=user, member_no_shares=randint(1, 99999), member_no_savings=randint(1, 99999), id_no=randint(1, 99999))
        return redirect('edit-member', id)

