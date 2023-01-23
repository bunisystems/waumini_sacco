from venv import create
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from pytz import timezone
from api.models import *
# Create your views here.
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count, Sum, F
from django.db.models.functions import TruncMonth
from django.db import connection
from .functions import dictfetchall
from datetime import datetime, timedelta, time, date
import datetime
from django.db.models.functions import Coalesce
from django.utils.timezone import make_aware
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users
from .constants import *
import calendar
from .functions import *
import decimal
from django.utils.timezone import make_aware
import pytz

# Create your views here.
def sign_in(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('index')

		else:
			messages.info(request, 'Username or password is incorrect')

	context = {}
	return render(request, 'expense/auth/sign-in.html', context)

def sign_out(request):
	logout(request)
	return redirect('sign-in')

def index(request):

    group = Group.objects.get(name='Member')
    """ Get the current date """
    today = datetime.now().date()
    tomorrow = today + timedelta(1)
    today_start = datetime.combine(today, time())
    today_end = datetime.combine(tomorrow, time())
    
    month = today + timedelta(30)
    m_today_start = datetime.combine(today, time())
    m_today_end = datetime.combine(month, time())

    """ Get the current month """
    this_month = datetime.now().month
    last_month = datetime.now().month - 1

    # USERS
    s_users = User.objects.all().exclude(groups=group).count()
    s_active_users = User.objects.filter(is_active=1).exclude(groups=group).count()
    s_inactive_users = User.objects.filter(is_active=0).exclude(groups=group).count()

    # MEMBERS
    s_members = User.objects.filter(groups=group).count()
    s_paid_reg = Registration.objects.filter(is_deleted=0).count()
    s_unpaid_reg = s_members - s_paid_reg

    # LOANS
    s_loans = Loan.objects.all().count()
    s_paid_loans = Loan.objects.filter(is_paid=1).aggregate(Sum('balance'))['balance__sum']
    s_unpaid_loans = Loan.objects.filter(is_paid=0).aggregate(Sum('balance'))['balance__sum']
    t_loans = Loan.objects.all().aggregate(Sum('total'))['total__sum']

    """ This/Last month's float """
    l_this_month = Loan.objects.filter(created_on__month=this_month).aggregate(Sum('total'))['total__sum']
    l_last_month = Loan.objects.filter(created_on__month=last_month).aggregate(Sum('total'))['total__sum']


    # Current Yr
    current_time = timezone.now()
    current_year = timezone.now().year
    start_date = current_time.replace(current_year, 1, 1)
    end_date = current_time.replace(current_year, 12, 31)

    """ Total Loans per Month Charts """
    lc_labels = []
    lc_data = []

    with connection.cursor() as cursor:
        cursor.execute("CALL sp_loan_per_month(%s, %s)",(start_date,end_date))
        loan_per_month = dictfetchall(cursor)
    

    for lpm in loan_per_month: 
        lc_labels.append(lpm['month'])
        lc_data.append(str(lpm['total_amount']))
    
    """ Total Loan per Year Charts """

    ly_labels = []
    ly_data = []

    with connection.cursor() as cursor:
        cursor.execute("CALL sp_loan_per_year")
        loan_per_year = dictfetchall(cursor)
    

    for lpy in loan_per_year: 
        ly_labels.append(int(lpy['year']))
        ly_data.append(str(lpy['total_amount']))
    
    trans = Payments.objects.all()[:5]
    
    
    context = {
        's_members' : s_members,
        's_paid_reg' : s_paid_reg,
        's_unpaid_reg' : s_unpaid_reg,
        's_loans' : s_loans,
        's_paid_loans' : s_paid_loans,
        's_unpaid_loans' : s_unpaid_loans,
        's_users' : s_users,
        's_active_users' : s_active_users,
        's_inactive_users' : s_inactive_users,
        't_loans' : t_loans,
        'l_this_month' : l_this_month,
        'l_last_month' : l_last_month,
        'lc_labels' : lc_labels,
        'lc_data' : lc_data,
        'ly_labels' : ly_labels,
        'ly_data' : ly_data,
        'trans' : trans
        }

    return render(request, 'sacco/index.html', context)

""" User """

def users(request):
    users = User.objects.all()
    context = {'users': users }
    return render(request, 'sacco/users/users.html', context)

def members(request):
    users = User.objects.all().exclude(is_superuser=1).exclude(is_staff=1)
    context = {'users': users }
    return render(request, 'sacco/users/members.html', context)

def add_user(request):
    form = CreateUserForm()
    groups = Group.objects.all()
    values = request.POST
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        email = request.POST['email']
        username = request.POST['username']

       
        print('Printing POST:', request.POST)
        print('Printing Errors:', form.errors )
        if num_length(username) != PHONE_NUMBER:
            messages.error(request, "Phone number number must have " + str(PHONE_NUMBER) + ' digits')    
        elif(starts_with_zero(username) == False):       
            messages.error(request, "Phone number number must begin with 0")    
        else:
            if form.is_valid():
               
                user = form.save(commit=False)
                user.save()

            
                username = form.cleaned_data.get('username')
    

                g = form.cleaned_data.get('group')

        
            
                print('selected user role:',g)
                
                if g == 'SystemAdmin':
                    g = Group.objects.get(name='SystemAdmin')
                    g.user_set.add(user)
                elif g == 'SystemAccountant':
                    g = Group.objects.get(name='SystemAccountant')
                    g.user_set.add(user)
                elif g == 'SystemUser':
                    g = Group.objects.get(name='SystemUser')
                    g.user_set.add(user)
                elif g == 'Member':
                    g = Group.objects.get(name='Member')
                    g.user_set.add(user)
                else:
                    messages.error(request,  username + " cannot be added to a group")
                    return redirect('member')
                    

                messages.success(request,  username + " has been created successfully")
                return redirect('members')
    else:
       
        form = CreateUserForm()

    
    context = {'groups': groups, 'form': form, 'values' : values}

    if groups:
        return render(request, 'sacco/users/add-user.html', context)
    else:
        messages.error(request,  "Error! Roles are not added, Please contact system administrator")
        return render(request, 'sacco/error.html', context)


def edit_user(request, id):
    user = User.objects.get(pk=id)

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM `auth_group`")
        groups = dictfetchall(cursor)

    context = {
        'groups': groups, 
        'values': user
        }
    
    if request.method == 'GET':
        return render(request, 'sacco/users/edit-user.html', context)

    if request.method == 'POST':
        e = request.POST['email']
        u = request.POST['username']

    

             
        # if User.objects.exclude(pk=id).filter(email=e):
        #     messages.error(request, "Email already exists")
        #     return render(request, 'sacco/users/edit-user.html', context)

        if User.objects.exclude(pk=id).filter(username=u):
            messages.error(request, "Phone number already exists")
        elif(num_length(u) != PHONE_NUMBER):
            messages.error(request, "Phone number number must have " + str(PHONE_NUMBER) + ' digits starting with 0') 
        elif(starts_with_zero(u) == False):       
            messages.error(request, "Phone number number must begin with 0")  
        else:
            email = request.POST['email']
            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            g = request.POST['group']

            print('selected user role:',g)


            with connection.cursor() as cursor:
                cursor.execute("call sp_update_user(%s, %s, %s, %s, %s, %s)", (id, username, first_name, last_name, email, g))
                data = cursor.fetchone()
                messages.success(request,  username + " has been updated successfully")
                return redirect('members')

    return render(request, 'sacco/users/edit-user.html', context)

def profile(request, id):
    user = User.objects.get(pk=id)

    if request.user.id == id:
        context = { 'values': user }

        if request.method == 'GET':
            return render(request, 'sacco/users/profile.html', context)

        if request.method == 'POST':
            e = request.POST['email']
            u = request.POST['username']
                
            if User.objects.exclude(pk=id).filter(email=e):
                messages.error(request, "Email already exists")
                return render(request, 'expense/users/profile.html', context)
            elif User.objects.exclude(pk=id).filter(username=u):
                messages.error(request, "Username already exists")
                return render(request, 'expense/users/profile.html', context)
            else:
                email = request.POST['email']
                username = request.POST['username']
                first_name = request.POST['first_name']
                last_name = request.POST['last_name']
            
                with connection.cursor() as cursor:
                    cursor.execute("call sp_update_profile(%s, %s, %s, %s, %s)", (id, username, first_name, last_name, email))
                    data = cursor.fetchone()
                    messages.success(request,  username + " has been updated successfully")
                    return redirect('profile', id)
        
        return render(request, 'sacco/users/profile.html', context)
    else:
        return render(request, 'sacco/access.html')

def member(request, id):
    user = User.objects.get(pk=id)
    registration = Registration.objects.filter(member=id)
    loan = Loan.objects.filter(member=id)
    context = { 
        'user': user , 
        'registration':registration,
        'loan': loan
    }
    return render(request, 'sacco/users/member.html', context)
  
def delete_user(request, id):
    with connection.cursor() as cursor:
        cursor.execute("call sp_delete_user(%s)", [id])
        data = cursor.fetchone()
        messages.success(request, 'User deleted')
        return redirect('users')

""" User End """


""" Registration """
def registration(request):
    registration = Registration.objects.all()
    context = { 'registration' : registration}
    return render(request, 'sacco/registration/registration.html', context)

def add_registration(request):
    members = User.objects.all().exclude(is_superuser=1).exclude(is_staff=1)

    context = {'values': request.POST, 'members' : members }

    print(request.POST)

    if request.method == 'GET':
        if members:
            return render(request, 'sacco/registration/add-registration.html', context)
        else:
            messages.error(request,  "Error! Pleae add sacco members")
            return render(request, 'sacco/error.html')

    # The view to handle the form POST requests
    if request.method == 'POST':
      
        amount = request.POST['amount']
        
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'sacco/registration/add-registration.html', context)
        
        if int(amount) != int(REGISTRATION_FEE):
            messages.error(request, 'Amount must be ' + str(REGISTRATION_FEE))
            return render(request, 'sacco/registration/add-registration.html', context)


        member = User.objects.get(id=request.POST.get('member'))

        if Registration.objects.filter(member=request.POST.get('member')):
            messages.error(request, 'Registration amount exists')
            return render(request, 'sacco/registration/add-registration.html', context)

        if not member:
            messages.error(request, 'Member is required')
            return render(request, 'sacco/registration/add-registration.html', context)
       
        # if no error we save the data into database
        # we use the expense model
        # create the expense
        Registration.objects.create( member=member, amount=amount, created_by=request.user)

        # saving the expense in the database after creating it
        messages.success(request, 'Registration Fee saved successfully')

        # redirect to the expense page to see the expenses
        return redirect('registration')

def edit_registration(request, id):
    registration = Registration.objects.get(pk=id)

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
            messages.error(request, 'Amount is required')
            return render(request, 'sacco/registration/edit-registration.html', context)
       
        registration.amount = amount
        registration.save()
    

        # saving the expense in the database after creating it
        messages.success(request, 'Registration Fee updated successfully')

        # redirect to the expense page to see the expenses
        return redirect('registration')


""" Loans """
def loan(request):
    registration = Loan.objects.filter(is_paid=0)
    context = { 'registration' : registration}
    return render(request, 'sacco/loan/loan.html', context)

def loan_info(request, id):
    loan = Loan.objects.get(pk=id)
    context = { 'loan' : loan }
    return render(request, 'sacco/loan/loan-info.html', context)

def add_loan(request):
    members = User.objects.all().exclude(is_superuser=1).exclude(is_staff=1)

    context = {'values': request.POST, 'members' : members }

    print(request.POST)

    if request.method == 'GET':
        if members:
            return render(request, 'sacco/loan/add-loan.html', context)
        else:
            messages.error(request,  "Error! Pleae add sacco members")
            return render(request, 'sacco/error.html')

    # The view to handle the form POST requests
    if request.method == 'POST':
      
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'sacco/loan/add-loan.html', context)
        
        if int(amount) < MIN_LOAN:
            messages.error(request, 'Min Loan is ' + str(MIN_LOAN))
            return render(request, 'sacco/loan/add-loan.html', context)
        
        if int(amount) > MAX_LOAN:
            messages.error(request, 'Max Loan is ' + str(MAX_LOAN))
            return render(request, 'sacco/loan/add-loan.html', context)

        loan_fee = request.POST['loan_fee']

        if not loan_fee:
            messages.error(request, 'Loan fee is required')
            return render(request, 'sacco/loan/add-loan.html', context)
        
        duration = request.POST['duration']

        if not duration:
            messages.error(request, 'Duration in months is required')
            return render(request, 'sacco/loan/add-loan.html', context)
        else:
            due_date = add_months(int(duration))

        interest = request.POST['interest']

        if not interest:
            messages.error(request, 'Error! interest is required')
            return render(request, 'sacco/loan/add-loan.html', context)

        total_interest =    (float(amount) * (float(INTEREST) / 100)) * float(duration)
        form_interest = float(interest) * float(duration)
        if  form_interest != total_interest:
            messages.error(request, 'Error! during interest calculation')
            return render(request, 'sacco/loan/add-loan.html', context)
        
        insurance = request.POST['insurance']

        if not insurance:
            messages.error(request, 'Error! insuarance is required')
            return render(request, 'sacco/loan/add-loan.html', context)
        
        total_insurance = float(amount) * (float(INSUARANCE) / 100)
        print(total_insurance)
        if  float(insurance) != total_insurance:
            messages.error(request, 'Error! during insurance calculation')
            return render(request, 'sacco/loan/add-loan.html', context)

        total = float(amount) + float(total_interest) + float(total_insurance) + float(loan_fee)
        
        


        member = User.objects.get(id=request.POST.get('member'))

        if not member:
            messages.error(request, 'Member is required')
            return render(request, 'sacco/loan/add-loan.html', context)

        
       
        # if no error we save the data into database
        # we use the expense model
        # create the expense
        Loan.objects.create( 
            member=member, 
            amount=amount, 
            interest_rate=INTEREST ,
            interest=total_interest,
            insuarance_rate=INSUARANCE, 
            insurance=total_insurance,
            loan_fee=loan_fee,
            due_date=due_date, 
            balance=total,
            months=duration,
            total=total, 
            is_paid = 0, 
            created_by=request.user)

        # saving the expense in the database after creating it
        messages.success(request, 'Loan Fee saved successfully')

        # redirect to the expense page to see the expenses]
        return redirect('loan')

def edit_loan(request, id):
    registration = Loan.objects.get(pk=id)

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
            messages.error(request, 'Amount is required')
            return render(request, 'sacco/registration/edit-registration.html', context)
       
        registration.amount = amount
        registration.save()
    

        # saving the expense in the database after creating it
        messages.success(request, 'Loan Fee updated successfully')

        # redirect to the expense page to see the expenses
        return redirect('loan')

def loan_payments(request, id):
    loan = Loan.objects.get(pk=id)
    context = { 'loan' : loan }
    print(request.POST)

    if request.method == 'GET':
        return render(request, 'sacco/loan/loan-payments.html', context)
    
    if request.method == 'POST':
        member = User.objects.get(id=request.POST.get('member'))
        if not member:
            messages.error(request, 'Member is required')
            return render(request, 'sacco/loan/loan-payments.html', context)
       
        loans = Loan.objects.get(id=request.POST.get('loan'))
        if not loans:
            messages.error(request, 'Loan is required')
            return render(request, 'sacco/loan/loan-payments.html', context)
        
      

        paid_amount = request.POST['amount']
        if not paid_amount:
            messages.error(request, 'Amount is required')
            return render(request, 'sacco/loan/loan-payments.html', context)
        elif(float(paid_amount) > loan.balance):
            messages.error(request, 'Amount cannot be greater than ' + str(loan.balance))
            return render(request, 'sacco/loan/loan-payments.html', context)
        else:
            paid = decimal.Decimal(paid_amount)
        

        Payments.objects.create( 
            loan=loan,
            member=member, 
            total=loan.total,
            balance=loan.balance, 
            paid=paid,
            created_by=request.user)

        # saving the expense in the database after creating it
       
        messages.success(request, 'Payments saved successfully')
        return redirect('loan')
    
    return render(request, 'sacco/loan/loan-payments.html', context)

def paid_loan(request):
    registration = Loan.objects.filter(is_paid=1)
    context = { 'registration' : registration}
    return render(request, 'sacco/loan/loan.html', context)

def unpaid_loan(request):
    registration = Loan.objects.filter(is_paid=0)
    context = { 'registration' : registration}
    return render(request, 'sacco/loan/loan.html', context)

""" Capital Shares """
def capital_shares(request):
    registration = CapitalShares.objects.all()
    context = { 'registration' : registration}
    return render(request, 'sacco/registration/registration.html', context)

def add_capital_shares(request):
    members = User.objects.all().exclude(is_superuser=1).exclude(is_staff=1)

    context = {'values': request.POST, 'members' : members }

    print(request.POST)

    if request.method == 'GET':
        if members:
            return render(request, 'sacco/registration/add-registration.html', context)
        else:
            messages.error(request,  "Error! Pleae add sacco members")
            return render(request, 'sacco/error.html')

    # The view to handle the form POST requests
    if request.method == 'POST':

      
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'sacco/registration/add-registration.html', context)

        if int(amount) != CAPITAL_SHARE:
            messages.error(request, 'Amount should be ' + str(CAPITAL_SHARE))
            return render(request, 'sacco/registration/add-registration.html', context)


        member = User.objects.get(id=request.POST.get('member'))

        if not member:
            messages.error(request, 'Member is required')
            return render(request, 'sacco/registration/add-registration.html', context)
        
        import datetime
        current_month = datetime.datetime.now().month
        """ Get the current date """
        today = datetime.datetime.now().date()
        tomorrow = today + timedelta(1)
        today_start = datetime.datetime.combine(today, time())
        today_end = datetime.datetime.combine(tomorrow, time())
        member_current_month = CapitalShares.objects.filter(member=member, created_on__range=(today_start, today_end))
        if member_current_month:
            messages.error(request, 'Payment for ' + str(calendar.month_abbr[current_month])  + ' exists')
            return render(request, 'sacco/registration/add-registration.html', context)
       
        # if no error we save the data into database
        # we use the expense model
        # create the expense
        CapitalShares.objects.create( member=member, amount=amount, created_by=request.user)

        # saving the expense in the database after creating it
        messages.success(request, 'Capital Shares Fee saved successfully')

        # redirect to the expense page to see the expenses
        return redirect('capital-shares')

def edit_capital_shares(request, id):
    registration = CapitalShares.objects.get(pk=id)

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
            messages.error(request, 'Amount is required')
            return render(request, 'sacco/registration/edit-registration.html', context)
        
        if float(amount) != float(CAPITAL_SHARE):
            messages.error(request, 'Amount should be ' + str(CAPITAL_SHARE))
            return render(request, 'sacco/registration/edit-registration.html', context)
       
        registration.amount = amount
        registration.save()
    

        # saving the expense in the database after creating it
        messages.success(request, 'Capital Shares Fee updated successfully')

        # redirect to the expense page to see the expenses
        return redirect('capital-shares')

"""  Shares """
def shares(request):
    registration = Shares.objects.all()
    context = { 'registration' : registration}
    return render(request, 'sacco/registration/registration.html', context)

def add_shares(request):
    members = User.objects.all().exclude(is_superuser=1).exclude(is_staff=1)

    context = {'values': request.POST, 'members' : members }

    print(request.POST)

    if request.method == 'GET':
        if members:
            return render(request, 'sacco/registration/add-registration.html', context)
        else:
            messages.error(request,  "Error! Pleae add sacco members")
            return render(request, 'sacco/error.html')

    # The view to handle the form POST requests
    if request.method == 'POST':

      
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'sacco/registration/add-registration.html', context)

        if int(amount) < SHARES_MIN:
            messages.error(request, 'Amount should not be less than ' + str(SHARES_MIN))
            return render(request, 'sacco/registration/add-registration.html', context)


        member = User.objects.get(id=request.POST.get('member'))

        if not member:
            messages.error(request, 'Member is required')
            return render(request, 'sacco/registration/add-registration.html', context)
        
       
       
        # if no error we save the data into database
        # we use the expense model
        # create the expense
        Shares.objects.create( member=member, amount=amount, created_by=request.user)

        # saving the expense in the database after creating it
        messages.success(request, 'shares Fee saved successfully')

        # redirect to the expense page to see the expenses
        return redirect('shares')

def edit_shares(request, id):
    registration = Shares.objects.get(pk=id)

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
            messages.error(request, 'Amount is required')
            return render(request, 'sacco/registration/edit-registration.html', context)
        
        if float(amount) < float(SHARES_MIN):
            messages.error(request, 'Amount should not be less than ' + str(SHARES_MIN))
            return render(request, 'sacco/registration/add-registration.html', context)

       
        registration.amount = amount
        registration.save()
    

        # saving the expense in the database after creating it
        messages.success(request, 'Shares Fee updated successfully')

        # redirect to the expense page to see the expenses
        return redirect('shares')

""" NHIF """
def nhif(request):
    registration = NHIF.objects.all()
    context = { 'registration' : registration}
    return render(request, 'sacco/registration/registration.html', context)

def add_nhif(request):
    members = User.objects.all().exclude(is_superuser=1).exclude(is_staff=1)

    context = {'values': request.POST, 'members' : members }

    print(request.POST)

    if request.method == 'GET':
        if members:
            return render(request, 'sacco/registration/add-registration.html', context)
        else:
            messages.error(request,  "Error! Pleae add sacco members")
            return render(request, 'sacco/error.html')

    # The view to handle the form POST requests
    if request.method == 'POST':
      
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'sacco/registration/add-registration.html', context)


        member = User.objects.get(id=request.POST.get('member'))

        if not member:
            messages.error(request, 'Member is required')
            return render(request, 'sacco/registration/add-registration.html', context)
       
        # if no error we save the data into database
        # we use the expense model
        # create the expense
        NHIF.objects.create( member=member, amount=amount, created_by=request.user)

        # saving the expense in the database after creating it
        messages.success(request, 'NHIF Fee saved successfully')

        # redirect to the expense page to see the expenses
        return redirect('nhif')

def edit_nhif(request, id):
    registration = NHIF.objects.get(pk=id)

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
            messages.error(request, 'Amount is required')
            return render(request, 'sacco/registration/edit-registration.html', context)
       
        registration.amount = amount
        registration.save()
    

        # saving the expense in the database after creating it
        messages.success(request, 'NHIF Fee updated successfully')

        # redirect to the expense page to see the expenses
        return redirect('nhif')


""" Cheque """
def cheque(request):
    registration = Cheque.objects.all()
    context = { 'registration' : registration}
    return render(request, 'sacco/registration/registration.html', context)

def add_cheque(request):
    members = User.objects.all().exclude(is_superuser=1).exclude(is_staff=1)

    context = {'values': request.POST, 'members' : members }

    print(request.POST)

    if request.method == 'GET':
        if members:
            return render(request, 'sacco/registration/add-registration.html', context)
        else:
            messages.error(request,  "Error! Pleae add sacco members")
            return render(request, 'sacco/error.html')

    # The view to handle the form POST requests
    if request.method == 'POST':
      
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'sacco/registration/add-registration.html', context)


        member = User.objects.get(id=request.POST.get('member'))

        if not member:
            messages.error(request, 'Member is required')
            return render(request, 'sacco/registration/add-registration.html', context)
       
        # if no error we save the data into database
        # we use the expense model
        # create the expense
        Cheque.objects.create( member=member, amount=amount, created_by=request.user)

        # saving the expense in the database after creating it
        messages.success(request, 'Cheque Fee saved successfully')

        # redirect to the expense page to see the expenses
        return redirect('cheque')

def edit_cheque(request, id):
    registration = Cheque.objects.get(pk=id)

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
            messages.error(request, 'Amount is required')
            return render(request, 'sacco/registration/edit-registration.html', context)
       
        registration.amount = amount
        registration.save()
    

        # saving the expense in the database after creating it
        messages.success(request, 'Cheque Fee updated successfully')

        # redirect to the expense page to see the expenses
        return redirect('cheque')


""" Account """
def account(request):
    registration = Account.objects.all()
    context = { 'registration' : registration}
    return render(request, 'sacco/registration/registration.html', context)

def add_account(request):
    members = User.objects.all().exclude(is_superuser=1).exclude(is_staff=1)

    context = {'values': request.POST, 'members' : members }

    print(request.POST)

    if request.method == 'GET':
        if members:
            return render(request, 'sacco/registration/add-registration.html', context)
        else:
            messages.error(request,  "Error! Pleae add sacco members")
            return render(request, 'sacco/error.html')

    


    # The view to handle the form POST requests
    if request.method == 'POST':
      
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'sacco/registration/add-registration.html', context)
        
        if int(amount) != ACCOUNT:
            messages.error(request, 'Amount should be ' + str(ACCOUNT))
            return render(request, 'sacco/registration/add-registration.html', context)


        member = User.objects.get(id=request.POST.get('member'))

        if not member:
            messages.error(request, 'Member is required')
            return render(request, 'sacco/registration/add-registration.html', context)
       
        # if no error we save the data into database
        # we use the expense model
        # create the expense
        Account.objects.create( member=member, amount=amount, created_by=request.user)

        # saving the expense in the database after creating it
        messages.success(request, 'Account Fee saved successfully')

        # redirect to the expense page to see the expenses
        return redirect('account')

def edit_account(request, id):
    registration = Account.objects.get(pk=id)

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
            messages.error(request, 'Amount is required')
            return render(request, 'sacco/registration/edit-registration.html', context)
        
        if float(amount) != float(ACCOUNT):
            messages.error(request, 'Amount should be ' + str(ACCOUNT))
            return render(request, 'sacco/registration/add-registration.html', context)
       
        registration.amount = amount
        registration.save()
    

        # saving the expense in the database after creating it
        messages.success(request, 'Account Fees updated successfully')

        # redirect to the expense page to see the expenses
        return redirect('account')


""" Processing Fee """
def processing(request):
    registration = Processing.objects.all()
    context = { 'registration' : registration}
    return render(request, 'sacco/registration/registration.html', context)

def add_processing(request):
    members = User.objects.all().exclude(is_superuser=1).exclude(is_staff=1)

    context = {'values': request.POST, 'members' : members }

    print(request.POST)

    if request.method == 'GET':

        if members:
            return render(request, 'sacco/registration/add-registration.html', context)
        else:
            messages.error(request,  "Error! Pleae add sacco members")
            return render(request, 'sacco/error.html')

    # The view to handle the form POST requests
    if request.method == 'POST':
      
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'sacco/registration/add-registration.html', context)
        

        if int(amount) != PROCESSING_FEE:
            messages.error(request, 'Amount should be ' + str(PROCESSING_FEE))
            return render(request, 'sacco/registration/add-registration.html', context)


        member = User.objects.get(id=request.POST.get('member'))

        if not member:
            messages.error(request, 'Member is required')
            return render(request, 'sacco/registration/add-registration.html', context)
       
        # if no error we save the data into database
        # we use the expense model
        # create the expense
        Processing.objects.create( member=member, amount=amount, created_by=request.user)

        # saving the expense in the database after creating it
        messages.success(request, 'Processing Fee saved successfully')

        # redirect to the expense page to see the expenses
        return redirect('processing')

def edit_processing(request, id):
    registration = Processing.objects.get(pk=id)

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
            messages.error(request, 'Amount is required')
            return render(request, 'sacco/registration/edit-registration.html', context)
        
        if float(amount) != float(PROCESSING_FEE):
            messages.error(request, 'Amount should be ' + str(PROCESSING_FEE))
            return render(request, 'sacco/registration/add-registration.html', context)
       
        registration.amount = amount
        registration.save()
    

        # saving the expense in the database after creating it
        messages.success(request, 'Processing Fee updated successfully')

        # redirect to the expense page to see the expenses
        return redirect('processing')



""" Passbook """
def passbook(request):
    registration = Passbook.objects.all()
    context = { 'registration' : registration}
    return render(request, 'sacco/registration/registration.html', context)

def add_passbook(request):
    members = User.objects.all().exclude(is_superuser=1).exclude(is_staff=1)

    context = {'values': request.POST, 'members' : members }

    print(request.POST)

    if request.method == 'GET':
        if members:
            return render(request, 'sacco/registration/add-registration.html', context)
        else:
            messages.error(request,  "Error! Pleae add sacco members")
            return render(request, 'sacco/error.html')

    # The view to handle the form POST requests
    if request.method == 'POST':
      
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'sacco/registration/add-registration.html', context)

        if float(amount) != float(PASSBOOK):
            messages.error(request, 'Amount should be ' + str(PASSBOOK))
            return render(request, 'sacco/registration/add-registration.html', context)


        member = User.objects.get(id=request.POST.get('member'))

        if not member:
            messages.error(request, 'Member is required')
            return render(request, 'sacco/registration/add-registration.html', context)
       
        # if no error we save the data into database
        # we use the expense model
        # create the expense
        Passbook.objects.create( member=member, amount=amount, created_by=request.user)

        # saving the expense in the database after creating it
        messages.success(request, 'Passbook Fee saved successfully')

        # redirect to the expense page to see the expenses
        return redirect('passbook')

def edit_passbook(request, id):
    registration = Passbook.objects.get(pk=id)

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
            messages.error(request, 'Amount is required')
            return render(request, 'sacco/registration/edit-registration.html', context)
        
        if float(amount) != float(PASSBOOK):
            messages.error(request, 'Amount should be ' + str(PASSBOOK))
            return render(request, 'sacco/registration/add-registration.html', context)
       
        registration.amount = amount
        registration.save()
    

        # saving the expense in the database after creating it
        messages.success(request, 'Passbook Fee updated successfully')

        # redirect to the expense page to see the expenses
        return redirect('passbook')
































































