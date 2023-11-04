from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from sacco.decorators import *
from django.core.paginator import Paginator
from api.models import Withdrawl
from pytz import timezone
from django.contrib import messages
from datetime import datetime, timedelta, time, date
from django.contrib.auth.models import Group
from sacco.constants import *
from django.db.models import Count, Sum, F
from api.models import *



try:
    group = Group.objects.get(name='Member')
except Exception as e:
    group = 'Member'


""" Account """
@login_required(login_url='sign-in')
def withdrawal(request):
    users = User.objects.filter(is_superuser=0, is_staff=0)
  
    if request.method == 'GET':
    
        registration = Withdrawl.objects.all()
        paginator = Paginator(registration, 20)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator, page_number)

        context = { 'registration' : registration, 'users' : users, 'page_obj': page_obj} 



        return render(request, 'sacco/registration/registration.html', context)
   
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
                return render(request, 'sacco/registration/r.html', context)
            else:
                registration = Withdrawl.objects.filter(created_on__range=(start_date, end_date), member=user)
                total = Withdrawl.objects.filter(created_on__range=(start_date, end_date), member=user).aggregate(Sum('amount'))['amount__sum']
               
                
                context = { 
                    'registration' : registration,
                    'total' : total,
                    'users': users,
                    'values' : request.POST
                    }
                return render(request, 'sacco/registration/r.html', context)

        return render(request, 'sacco/registration/registration.html', context)
    


@login_required(login_url='sign-in')
def add_withdrawal(request):
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
        
        last_statement = Statement.objects.filter(member=member).order_by('-created_on').first()
        if last_statement:
            if last_statement.balance < Decimal(amount):
                messages.error(request, "Insufficient Account Balance")
                return render(request, 'sacco/registration/add-registration.html', context)
        else:
            messages.error(request, "Insufficient Account Balance")
            return render(request, 'sacco/registration/add-registration.html', context)
    

    
        
    
        # if no error we save the data into database
        # we use the expense model
        # create the expense
        Withdrawl.objects.create( member=member, amount=amount, created_by=request.user)

        # saving the expense in the database after creating it
        messages.success(request, SUCCESS_FEE_SAVED)

        # redirect to the expense page to see the expenses
        return redirect('account')
@login_required(login_url='sign-in')
def edit_withdrawal(request, id):
    try:
        registration = Withdrawl.objects.get(pk=id)
    except Withdrawl.DoesNotExist:
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
        
        member = registration.member
        last_statement = Statement.objects.filter(member=member).order_by('-created_on').first()
        if last_statement:
            if last_statement.balance < Decimal(amount):
                messages.error(request, "Insufficient Account Balance")
                return render(request, 'sacco/registration/add-registration.html', context)
        else:
            messages.error(request, "Insufficient Account Balance")
            return render(request, 'sacco/registration/add-registration.html', context)
    
       
        registration.amount = amount
        registration.updated_by = request.user
        registration.updated_on = timezone.now()
        registration.save()
    

        # saving the expense in the database after creating it
        messages.success(request, SUCCESS_FEE_EDITED)

        # redirect to the expense page to see the expenses
        return redirect('account')


@login_required(login_url='sign-in')
def statement(request, member_id):
    account_statement = Statement.objects.filter(member=member_id).order_by('-created_on')
    
    context = { 'account_statement' : account_statement}
    return render(request, 'sacco/savings/statement.html', context)


@login_required(login_url='sign-in')
def withdrawl_reciept(request, withdrawal_id):
    r = Withdrawl.objects.get(pk=withdrawal_id)
    context = { 'r' : r}
    return render(request, 'sacco/reciept/r1.html', context)
