
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from sacco.decorators import *
from django.core.paginator import Paginator
from api.models import NHIF
from pytz import timezone
from django.contrib import messages
from datetime import datetime, timedelta, time, date
from django.contrib.auth.models import Group
from sacco.constants import *
from django.db.models import Count, Sum, F
from django.db.models import Q


try:
    group = Group.objects.get(name='Member')
except Exception as e:
    group = 'Member'


""" NHIF """
@login_required(login_url='sign-in')
def nhif(request):

    users = User.objects.filter(Q(groups=group)).prefetch_related('groups')
  
    if request.method == 'GET':

        registration = NHIF.objects.all()
        context = { 'registration' : registration, 'users' : users} 
        return render(request, 'sacco/nhif/nhif.html', context)
   
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
                return render(request, 'sacco/nhif/n.html', context)
            else:
                registration = NHIF.objects.filter(created_on__range=(start_date, end_date), member=user)
                total = NHIF.objects.filter(created_on__range=(start_date, end_date), member=user).aggregate(total=Sum(F('amount')) + Sum(F('commission')))['total']
               
                
                context = { 
                    'registration' : registration,
                    'total' : total,
                    'users': users,
                    'values' : request.POST
                    }
                return render(request, 'sacco/nhif/n.html', context)

        return render(request, 'sacco/nhif/nhif.html', context)

@login_required(login_url='sign-in')
def add_nhif(request):
    try:
        members = User.objects.filter(groups=group)
    
        context = {'values': request.POST, 'members' : members }

        print(request.POST)

        if request.method == 'GET':
            if members:
                return render(request, 'sacco/nhif/add-nhif.html', context)
            else:
                messages.error(request,  MEMBERS_EXIST)
                return render(request, 'sacco/error.html')

        # The view to handle the form POST requests
        if request.method == 'POST':
        
            amount = request.POST['amount']
            if not amount:
                messages.error(request, ERROR_AMOUNT)
                return render(request, 'sacco/nhif/add-nhif.html', context)


            member = User.objects.get(id=request.POST.get('member'))
            if not member:
                messages.error(request, ERROR_REG_MEMBER)
                return render(request, 'sacco/nhif/add-nhif.html', context)
            
            commission = request.POST['commission']
            if not commission:
                messages.error(request, ERROR_AMOUNT)
                return render(request, 'sacco/nhif/add-nhif.html', context)
            
            
        
    
            NHIF.objects.create( 
                member=member, 
                amount=amount, 
                commission=commission,
                created_by=request.user)

            
            messages.success(request, SUCCESS_FEE_SAVED)

            
            return redirect('nhif')
    except User.DoesNotExist:
        context = {'values': request.POST, 'members' : members }

        print(request.POST)

        if request.method == 'GET':
            if members:
                return render(request, 'sacco/nhif/add-nhif.html', context)
            else:
                messages.error(request,  MEMBERS_EXIST)
                return render(request, 'sacco/error.html')

        # The view to handle the form POST requests
        if request.method == 'POST':
        
            amount = request.POST['amount']
            if not amount:
                messages.error(request, ERROR_AMOUNT)
                return render(request, 'sacco/nhif/add-nhif.html', context)


            member = request.POST.get('member')
            if member != '0':
                messages.error(request, "Something went wrong")
                return render(request, 'sacco/nhif/add-nhif.html', context)
            
            commission = request.POST['commission']
            if not commission:
                messages.error(request, ERROR_AMOUNT)
                return render(request, 'sacco/nhif/add-nhif.html', context)

            
            f_name = request.POST['first_name']
            
            if not f_name:
                messages.error(request, ERROR_F_L_REQUIRED)  
                return render(request, 'sacco/nhif/add-nhif.html', context)  
            
            l_name = request.POST['last_name']

            if not l_name:
                messages.error(request, ERROR_F_L_REQUIRED)  
                return render(request, 'sacco/nhif/add-nhif.html', context)  

            number = request.POST['number']

            if num_length(number) != PHONE_NUMBER:
                messages.error(request, "Phone number number must have " + str(PHONE_NUMBER) + ' digits')    
                return render(request, 'sacco/nhif/add-nhif.html', context)
            elif(NHIF.objects.filter(phone_number=number)):
                messages.error(request, "Phone number exists") 
                return render(request, 'sacco/nhif/add-nhif.html', context) 

            
            id_no = request.POST['id_no']
            if not id_no:
                messages.error(request, ERROR_ID_NO_REQUIRED)  
                return render(request, 'sacco/nhif/add-nhif.html', context) 
            elif(NHIF.objects.filter(id_no=id_no)):
                messages.error(request, "ID number exists") 
                return render(request, 'sacco/nhif/add-nhif.html', context) 
            
    
            NHIF.objects.create( 
                amount=amount, 
                commission=commission,
                f_name=f_name,
                l_name=l_name,
                id_no=id_no,
                phone_number=number,
                is_member=member,
                created_by=request.user)

            
            messages.success(request, SUCCESS_FEE_SAVED)

            
            return redirect('nhif')

@login_required(login_url='sign-in')
def edit_nhif(request, id):
    try:
        registration = NHIF.objects.get(pk=id)
    except NHIF.DoesNotExist:
        messages.error(request, ERROR_404)
        return render(request, 'sacco/error.html')

    next_page = request.GET.get('nxt')

    context = {
        'values': registration, 
        'registration' : registration,
        'next_page' : next_page
    }

    
    
    if request.method == 'GET':
        return render(request, 'sacco/nhif/edit-nhif.html', context)

    # The view to handle the form POST requests
    if request.method == 'POST':
      
        amount = request.POST['amount']

        if not amount:
            messages.error(request, ERROR_AMOUNT)
            return render(request, 'sacco/nhif/edit-nhif.html', context)
        
        commission = request.POST['commission']
        if not commission:
            messages.error(request, ERROR_AMOUNT)
            return render(request, 'sacco/nhif/add-nhif.html', context)
        
       
        if next_page:
            registration.amount = amount
            registration.commission = commission
            registration.updated_by = request.user
            registration.updated_on = timezone.now()
            registration.save()
        

            # saving the expense in the database after creating it
            messages.success(request, SUCCESS_FEE_EDITED)

            # redirect to the expense page to see the expenses
            return redirect('nhif' )
        else:
            registration.amount = amount
            registration.commission = commission
            registration.updated_by = request.user
            registration.updated_on = timezone.now()
            registration.save()
        

            # saving the expense in the database after creating it
            messages.success(request, SUCCESS_FEE_EDITED)

            # redirect to the expense page to see the expenses
            return redirect('nhif' )

@login_required(login_url='sign-in')
def nhif_reciept(request, id):
    r = NHIF.objects.get(pk=id)
    context = { 'r' : r}
    return render(request, 'sacco/reciept/r1.html', context)
