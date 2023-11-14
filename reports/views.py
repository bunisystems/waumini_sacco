
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
from api.models import Withdrawl


try:
    group = Group.objects.get(name='Member')
except Exception as e:
    group = 'Member'

@login_required(login_url='sign-in')
def members(request):
    users = User.objects.filter(is_superuser=0, is_staff=0).select_related('userprofile').values('id', 'first_name', 'last_name', 'username', 'userprofile__member_no_shares', 'userprofile__member_no_savings', 'userprofile__id_no')
    page_obj = users
    context = {'users': users, 'page_obj': page_obj }
    return render(request, 'sacco/users/members.html', context)


@login_required(login_url='sign-in') 
def registration(request):

    users = User.objects.filter(Q(groups=group)).prefetch_related('groups')
    registration = Registration.objects.all()
    context = { 'registration' : registration, 'users' : users} 
    return render(request, 'sacco/reg/registration.html', context)


""" Capital Shares """
@login_required(login_url='sign-in')
def capital_shares(request):
    users = User.objects.filter(is_superuser=0, is_staff=0)
  
    registration = CapitalShares.objects.all()
    page_obj = registration


    context = { 'registration' : registration, 'users' : users, 'page_obj': page_obj} 
    return render(request, 'sacco/reports/r.html', context)


@login_required(login_url='sign-in')
def nhif(request):

    users = User.objects.filter(Q(groups=group)).prefetch_related('groups')
  
    registration = NHIF.objects.all()
    context = { 'registration' : registration, 'users' : users} 
    return render(request, 'sacco/nhif/nhif.html', context)


"""  Shares """
@login_required(login_url='sign-in')
def shares(request):
    users = User.objects.filter(Q(groups=group)).prefetch_related('groups')
  
    registration = Shares.objects.all()

    page_obj = registration

    
    context = { 'registration' : registration, 'users' : users, 'page_obj': page_obj} 
    return render(request, 'sacco/reports/r.html', context)


""" Account """
@login_required(login_url='sign-in')
def account(request):
    users = User.objects.filter(is_superuser=0, is_staff=0)
  
    registration = Account.objects.all()
    
    page_obj = registration

    context = { 'registration' : registration, 'users' : users, 'page_obj': page_obj} 

    return render(request, 'sacco/reports/r.html', context)


""" Account """
@login_required(login_url='sign-in')
def withdrawal(request):
    users = User.objects.filter(is_superuser=0, is_staff=0)

    registration = Withdrawl.objects.all()
    paginator = Paginator(registration, 20)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    context = { 'registration' : registration, 'users' : users, 'page_obj': page_obj} 

    return render(request, 'sacco/reports/r.html', context)
   

""" Cheque """
@login_required(login_url='sign-in')
def cheque(request):
    users = User.objects.filter(Q(groups=group)).prefetch_related('groups')

    registration = Cheque.objects.all()
    context = { 'registration' : registration, 'users' : users} 
    return render(request, 'sacco/cheque/cheque.html', context)


""" Passbook """
@login_required(login_url='sign-in')
def passbook(request):

    users = User.objects.filter(is_superuser=0, is_staff=0)

    registration = Passbook.objects.all()
    page_obj = registration

    context = { 'registration' : registration, 'users' : users, 'page_obj': page_obj} 
    return render(request, 'sacco/registration/registration.html', context)
   
 
   



   


