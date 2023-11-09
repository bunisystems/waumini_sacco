from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from sacco.decorators import *
from django.core.paginator import Paginator
from .models import Account_Deposit
from pytz import timezone
from django.contrib import messages
from datetime import datetime, timedelta, time, date
from django.contrib.auth.models import Group
from sacco.constants import *
from django.db.models import Count, Sum, F




try:
    group = Group.objects.get(name='Member')
except Exception as e:
    group = 'Member'

""" READ"""
@login_required(login_url='sign-in')
def deposits(request):
    users = User.objects.filter(is_superuser=0, is_staff=0)
  
    if request.method == 'GET':
    
        registration = Account_Deposit.objects.all()
        paginator = Paginator(registration, 20)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator, page_number)

        context = { 'registration' : registration, 'users' : users, 'page_obj': page_obj} 



        return render(request, 'sacco/deposit/deposits.html', context)
   
    print(request.POST)


    if request.method == 'POST':
        user = request.POST['user']
        start = request.POST['start']
        start_date = datetime.strptime(start, "%m/%d/%Y").strftime("%Y-%m-%d")
        end = request.POST['end']
        end_date = datetime.strptime(end, "%m/%d/%Y").strftime("%Y-%m-%d")

        if user:
            if start_date == end_date:
                messages.error(request, 'Start Date and End Date are similar')
                return render(request, 'sacco/registration/receipt.html', context)
            else:
                registration = Account_Deposit.objects.filter(created_on__range=(start_date, end_date), member=user)
                total = Account_Deposit.objects.filter(created_on__range=(start_date, end_date), member=user).aggregate(Sum('amount'))['amount__sum']
               
                
                context = { 
                    'registration' : registration,
                    'total' : total,
                    'users': users,
                    'values' : request.POST
                    }
                return render(request, 'sacco/registration/receipt.html', context)

        return render(request, 'sacco/registration/registration.html', context)
@login_required(login_url='sign-in')
def add_deposit(request):
    members = User.objects.filter(groups=group)

    context = {'values': request.POST, 'members' : members }

    print(request.POST)

    if request.method == 'GET':
        if members:
            return render(request, 'sacco/registration/add-registration.html', context)
        else:
            messages.error(request,  MEMBERS_EXIST)
            return render(request, 'sacco/error.html')

    


    # The view to handle the form POST requests
    if request.method == 'POST':
      
        amount = request.POST['amount']

        if not amount:
            messages.error(request, ERROR_AMOUNT)
            return render(request, 'sacco/registration/add-registration.html', context)
        
        # if int(amount) != ACCOUNT:
        #     messages.error(request,ERROR_INC_AMOUNT + str(ACCOUNT))
        #     return render(request, 'sacco/registration/add-registration.html', context)


        member = User.objects.get(id=request.POST.get('member'))

        if not member:
            messages.error(request, ERROR_REG_MEMBER)
            return render(request, 'sacco/registration/add-registration.html', context)
       
        # if no error we save the data into database
        # we use the expense model
        # create the expense
        Account_Deposit.objects.create( member=member, amount=amount, created_by=request.user)

        # saving the expense in the database after creating it
        messages.success(request, SUCCESS_FEE_SAVED)

        # redirect to the expense page to see the expenses
        return redirect('account')
@login_required(login_url='sign-in')
def edit_deposit(request, id):
    try:
        registration = Account_Deposit.objects.get(pk=id)
    except Account_Deposit.DoesNotExist:
        messages.error(request, ERROR_404)
        return render(request, 'sacco/error.html')

    context = {
        'values': registration, 
        'registration' : registration 
    }

    if request.method == 'GET':
        return render(request, 'sacco/registration/edit-registration.html', context)

    # The view to handle the form POST requests
    if request.method == 'POST':
      
        amount = request.POST['amount']

        if not amount:
            messages.error(request, ERROR_AMOUNT)
            return render(request, 'sacco/registration/edit-registration.html', context)
    
       
        registration.amount = amount
        registration.updated_by = request.user
        registration.updated_on = timezone.now()
        registration.save()
    

        # saving the expense in the database after creating it
        messages.success(request, SUCCESS_FEE_EDITED)

        # redirect to the expense page to see the expenses
        return redirect('account')


@login_required(login_url='sign-in')
def deposit_receipt(request, id):
    r = Account_Deposit.objects.get(pk=id)
    context = { 'r' : r}
    return render(request, 'sacco/reciept/r1.html', context)
