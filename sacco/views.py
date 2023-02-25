
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from pytz import timezone
from api.models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count, Sum, F
from django.db.models.functions import TruncMonth
from django.db import connection
from .functions import dictfetchall
from datetime import datetime, timedelta, time, date
import datetime
from django.contrib.auth.models import Group
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import *
import calendar
from .functions import *
import decimal
from django.utils.timezone import make_aware
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from random import randint
from django.core.cache import cache
from.celery import *
from django.db.models import Q
from .constants import *


try:
    group = Group.objects.get(name='Member')
except Exception as e:
    group = 'Member'

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

@unauthenticated_user
def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        next_page = request.GET.get('next')
        
        if user is not None:
            if next_page:
                login(request, user)
                return redirect(next_page)
            else:
                login(request, user)
                return redirect('index')    
        else:
            messages.info(request, 'Username or password is incorrect')
            
    context = {}
    return render(request, 'sacco/auth/sign-in.html', context)

def sign_out(request):
	logout(request)
	return redirect('sign-in')


@cache_page(CACHE_TTL)
@login_required(login_url='sign-in')
def index(request):

    # 2023-02-01
    today = timezone.now().date()
    # 2023-02-02
    tomorrow = today + timedelta(1)
    
    today_start = timezone.now().combine(today, time())

   
    
    today_end = timezone.now().combine(tomorrow, time())

    
    this_year =  datetime.now().year
    last_year =  datetime.now().year - 1

    month = today + timedelta(30)
    m_today_start = datetime.combine(today, time())
    m_today_end = datetime.combine(month, time())

    """ Get the current month """
    this_month = datetime.now().month
    last_month = datetime.now().month - 1

    # USERS
    group = Group.objects.get(name='Member')
    s_users = User.objects.filter(is_superuser=0).exclude(groups=group).count()
    s_active_users = User.objects.filter(is_active=1, is_superuser=0).exclude(groups=group).count()
    s_inactive_users = User.objects.filter(is_active=0, is_superuser=0).exclude(groups=group).count()

    # MEMBERS
    s_members = User.objects.filter(groups=group).count()
    s_paid_reg = Registration.objects.filter(is_deleted=0).count()
    s_unpaid_reg = s_members - s_paid_reg

    # LOANS
    s_loans = Loan.objects.all().count()
    s_paid_loans = Loan.objects.filter(is_paid=1).aggregate(Sum('total'))['total__sum']
    s_unpaid_loans = Loan.objects.filter(is_paid=0).aggregate(Sum('balance'))['balance__sum']
    t_loans = Loan.objects.all().aggregate(Sum('total'))['total__sum']

    """ This/Last month's Loans """
    l_this_month = Loan.objects.filter(created_on__month=this_month).aggregate(Sum('total'))['total__sum']
    l_last_month = Loan.objects.filter(created_on__month=last_month).aggregate(Sum('total'))['total__sum']

    """ This/Last Year's Loans """
    l_this_year = Loan.objects.filter(created_on__year=this_year).aggregate(Sum('total'))['total__sum']
    l_last_year = Loan.objects.filter(created_on__year=last_year).aggregate(Sum('total'))['total__sum']


    # Current Yr
    # 09:11:57.225475+00:00
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
    
    trans = Payments.objects.all().order_by('-created_on')[:5]
    
    
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
        'l_this_year': l_this_year, 
        'l_last_year': l_last_year,
        'lc_labels' : lc_labels,
        'lc_data' : lc_data,
        'ly_labels' : ly_labels,
        'ly_data' : ly_data,
        'trans' : trans
        }

    return render(request, 'sacco/index.html', context)

""" User """

@clear_cache
@cache_page(CACHE_TTL)
@login_required(login_url='sign-in')
def users(request):
    users = User.objects.filter(is_active=1, is_superuser=0)
    context = {'users': users }
    return render(request, 'sacco/users/users.html', context)

@login_required(login_url='sign-in')
def add_user(request):
    form = CreateUserForm()
    #groups = Group.objects.all().exclude(name="Member")
    groups = Group.objects.all()
    values = request.POST
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        email = request.POST['email']
        username = request.POST['username']
        
        print('Printing POST:', request.POST)
        print('Printing Errors:', form.errors )
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
        else:
            if form.is_valid():
                user = form.save(commit=False)
                user.password = User.objects.make_random_password()
                user.is_active = 1
                user.save()

                username = form.cleaned_data.get('username')
    
                g = form.cleaned_data.get('group')


                print('selected user role:',g)
            
                group = Group.objects.get(id=g)
                # Add user to group
                user.groups.add(group)

                # send_account_creation_email(email, f_name, l_name, username, url)

                messages.success(request,  username + " has been created successfully")
                cache.clear()
                return redirect('users')
                
    else:
       
        form = CreateUserForm()

    
    context = {'groups': groups, 'form': form, 'values' : values}

    if groups:
        return render(request, 'sacco/users/add-user.html', context)
    else:
        messages.error(request,  "Error! Roles are not added, Please contact system administrator")
        return render(request, 'sacco/error.html', context)

@login_required(login_url='sign-in')
def edit_user(request, id):
    try:
        user = User.objects.get(pk=id)
    except User.DoesNotExist:
        messages.error(request, ERROR_404)
        return render(request, 'sacco/error.html')

    #groups = Group.objects.all().exclude(name="Member")
    groups = Group.objects.all()

    context = {
        'groups': groups, 
        'values': user
        }
    
    if request.method == 'GET':
        return render(request, 'sacco/users/edit-user.html', context)

    if request.method == 'POST':
        e = request.POST['email']
        u = request.POST['username']



        if User.objects.exclude(pk=id).filter(email=e):
            messages.error(request, "Email already exists")
            return render(request, 'sacoo/users/edit-user.html', context)
        elif User.objects.exclude(pk=id).filter(username=u):
            messages.error(request, "Username already exists")
            return render(request, 'sacoo/users/edit-user.html', context)
        else:
            
             # Get user information from form
            user.username = request.POST['username']
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            user.password = User.objects.make_random_password()

            # Save user
            user.save()
            # Remove user from group           
            user.groups.set([])
            
            g  = request.POST['group']
            group = Group.objects.get(id=g)
            # Add user to group
            user.groups.add(group)

            print('selected user role:',g)
          
            messages.success(request,  user.username + " has been updated successfully")
            cache.clear()
            return redirect('users')

    return render(request, 'sacco/users/edit-user.html', context)


@login_required(login_url='sign-in')
def profile(request, id):
    try:
        user = User.objects.get(pk=id)
    except User.DoesNotExist:
        messages.error(request, ERROR_404)
        return render(request, 'sacco/error.html')

    groups = Group.objects.all().exclude(name="Member")

    context = {
        'groups': groups, 
        'values': user
        }
    
    if request.method == 'GET':
        return render(request, 'sacco/users/profile.html', context)

    if request.method == 'POST':
        e = request.POST['email']
        u = request.POST['username']



        if User.objects.exclude(pk=id).filter(email=e):
            messages.error(request, "Email already exists")
            return render(request, 'sacco/users/profile.html', context)
        elif User.objects.exclude(pk=id).filter(username=u):
            messages.error(request, "Username already exists")
            return render(request, 'sacco/users/profile.html', context)
        else:
            
             # Get user information from form
            user.username = request.POST['username']
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
           

            # Save user
            user.save()
            # Remove user from group           
            user.groups.set([])
            

          
            messages.success(request, "Profile has been updated successfully")
            cache.clear()
            return redirect('profile', user.id)

@login_required(login_url='sign-in')
def delete_user(request, id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("call sp_delete_user(%s)", [id])
            data = cursor.fetchone()
            messages.success(request, 'Deleted')
            cache.clear()
            return redirect('users')
    except:
        messages.error(request, ERROR_PK_CONSTRAINT)
        return render(request, 'sacco/error.html')

""" User End """

""" Add Member """
@login_required(login_url='sign-in')
def members(request):
    users = User.objects.filter(Q(groups=group)).prefetch_related('groups')
    context = {'users': users }
    return render(request, 'sacco/users/members.html', context)

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
        id_number = request.POST['id_no']
        
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
        return render(request, 'sacco/users/add-member.html', context)
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

    user_profile = UserProfileForm(request.POST, instance=user.userprofile)
    """ try:
        user_profile = UserProfileForm(request.POST, instance=user.userprofile)
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=user, member_no=randint(1, 99999))
        return redirect('members') """

    context = {
        'groups': groups, 
        'values': user,
        'user_profile' : user_profile,
        }
    


    if request.method == 'GET':
        return render(request, 'sacco/users/edit-member.html', context)

    if request.method == 'POST':
        e = request.POST['email']
        u = request.POST['username']
        member_no_shares = request.POST['member_no_shares']
        member_no_savings = request.POST['member_no_savings']
        is_active = request.POST['is_active']

        if not is_active:
            messages.error(request, "Is Member is required")
            return render(request, 'sacco/users/edit-member.html', context)

        if User.objects.exclude(pk=id).filter(email=e):
            messages.error(request, MEMBER_EMAIL_EXISTS)
            return render(request, 'sacco/users/edit-member.html', context)

        if User.objects.exclude(pk=id).filter(username=u):
            messages.error(request, "Phone number already exists")
        elif(num_length(u) != PHONE_NUMBER):
            messages.error(request, "Phone number number must have " + str(PHONE_NUMBER) + ' digits starting with 0') 
        elif(starts_with_zero(u) == False):       
            messages.error(request, "Phone number number must begin with 0")  
        elif not (member_no_shares) and (member_no_savings):
            messages.error(request, "Member Number is required")
        elif(UserProfile.objects.filter(member_no_shares=member_no_shares, member_no_savings=member_no_savings)).exclude(member_no_shares=member_no_shares, member_no_savings=member_no_savings):
            messages.error(request, "Member Number Exists")
        else:
            # Get user information from form
            user.username = request.POST['username']
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = f'user{randint(1, 99999)}@example.com'
            user.password = User.objects.make_random_password()
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

            if UserProfileForm.is_valid:
                user_profile.save()

            
            cache.clear()
            messages.success(request,  user.username + " has been updated successfully")
            return redirect('members')

    return render(request, 'sacco/users/edit-member.html', context)


""" Member End """

""" Registration """
@login_required(login_url='sign-in') 
def registration(request):

    users = User.objects.filter(Q(groups=group)).prefetch_related('groups')
  
    if request.method == 'GET':

        registration = Registration.objects.all()
        context = { 'registration' : registration, 'users' : users} 
        return render(request, 'sacco/reg/registration.html', context)
   
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
                return render(request, 'sacco/reg/registration.html', context)
            else:
                registration = Registration.objects.filter(created_on__range=(start_date, end_date), member=user)
               
                
                context = { 
                    'registration' : registration,
                  
                    'users': users,
                    'values' : request.POST
                    }
                return render(request, 'sacco/reg/registration.html', context)

        return render(request, 'sacco/reg/registration.html', context)


@login_required(login_url='sign-in')
def add_registration(request):
    members = User.objects.filter(groups=group)

    context = {'values': request.POST, 'members' : members }

    print(request.POST)

    if request.method == 'GET':
        if members:
            return render(request, 'sacco/reg/add-registration.html', context)
        else:
            messages.error(request,  MEMBERS_EXIST)
            return render(request, 'sacco/error.html')

    # The view to handle the form POST requests
    if request.method == 'POST':
      
        shares_entrance_fee = request.POST['shares_entrance_fee']
        
        if not shares_entrance_fee:
            shares_entrance_fee = 0
            #messages.error(request, ERROR_AMOUNT)
            #return render(request, 'sacco/reg/add-registration.html', context)
        
        else:

            if int(shares_entrance_fee) != int(SHARES_ENTRANCE_FEE):
                messages.error(request, ERROR_SEF_AMOUNT + str(SHARES_ENTRANCE_FEE) )
                return render(request, 'sacco/reg/add-registration.html', context)

        
        shares_application_fee = request.POST['shares_application_fee']
        
        if not shares_application_fee:
            #messages.error(request, ERROR_AMOUNT)
            #return render(request, 'sacco/reg/add-registration.html', context)
            shares_application_fee = 0
        
        else: 
            if int(shares_application_fee) != int(SHARES_APPLICATION_FEE):
                messages.error(request, ERROR_SAF_AMOUNT + str(SHARES_APPLICATION_FEE) )
                return render(request, 'sacco/reg/add-registration.html', context)
        
        savings_entrance_fee = request.POST['savings_entrance_fee']
        
        if not savings_entrance_fee:
            savings_entrance_fee = 0
            #messages.error(request, ERROR_AMOUNT)
            #return render(request, 'sacco/reg/add-registration.html', context)
    
        else:
            if int(savings_entrance_fee) != int(SAVINGS_ENTRANCE_FEE):
                messages.error(request, ERROR_SaEF_AMOUNT + str(SAVINGS_ENTRANCE_FEE) )
                return render(request, 'sacco/reg/add-registration.html', context)


        member = User.objects.get(id=request.POST.get('member'))

        if Registration.objects.filter(member=request.POST.get('member')):
            messages.error(request, ERROR_REG_EXISTS)
            return render(request, 'sacco/reg/add-registration.html', context)

        if not member:
            messages.error(request, ERROR_REG_MEMBER)
            return render(request, 'sacco/reg/add-registration.html', context)
       
        # if no error we save the data into database
        # we use the expense model
        # create the expense
        Registration.objects.create( 
            member=member, 
            shares_entrance_fee=shares_entrance_fee,
            shares_application_fee=shares_application_fee,
            savings_entrance_fee=savings_entrance_fee,
            created_by=request.user)

        # saving the expense in the database after creating it
        messages.success(request, SUCCESS_FEE_SAVED)

        # redirect to the expense page to see the expenses
        return redirect('registration')
    
@login_required(login_url='sign-in')
def edit_registration(request, id):
    try:
        registration = Registration.objects.get(pk=id)
    except Registration.DoesNotExist:
        messages.error(request, ERROR_404)
        return render(request, 'sacco/error.html')
    members = User.objects.all().exclude(is_superuser=1).exclude(is_staff=1)

    context = {
        'values': registration, 
        'registration' : registration,
        'members' : members
    }

    if request.method == 'GET':
        return render(request, 'sacco/reg/edit-registration.html', context)

    # The view to handle the form POST requests
    if request.method == 'POST':
      
        shares_entrance_fee = request.POST['shares_entrance_fee']
        
        if not shares_entrance_fee:
            shares_entrance_fee = 0
            # messages.error(request, ERROR_AMOUNT)
            # return render(request, 'sacco/reg/edit-registration.html', context)
        
        """ if int(float(shares_entrance_fee)) != int(SHARES_ENTRANCE_FEE):
            messages.error(request, ERROR_SEF_AMOUNT + str(SHARES_ENTRANCE_FEE) )
            return render(request, 'sacco/reg/edit-registration.html', context) """
        
        shares_application_fee = request.POST['shares_application_fee']
        
        if not shares_application_fee:
            shares_application_fee = 0
            # messages.error(request, ERROR_AMOUNT)
            # return render(request, 'sacco/reg/edit-registration.html', context)
        
        # if int(float(shares_application_fee)) != int(SHARES_APPLICATION_FEE):
        #     messages.error(request, ERROR_SAF_AMOUNT + str(SHARES_APPLICATION_FEE) )
        #     return render(request, 'sacco/reg/edit-registration.html', context)
        
        savings_entrance_fee = request.POST['savings_entrance_fee']
        
        if not savings_entrance_fee:
            savings_entrance_fee = 0
            # messages.error(request, ERROR_AMOUNT)
            # return render(request, 'sacco/reg/edit-registration.html', context)
        
        """ if int(float(savings_entrance_fee)) != int(SAVINGS_ENTRANCE_FEE):
            messages.error(request, ERROR_SaEF_AMOUNT + str(SAVINGS_ENTRANCE_FEE) )
            return render(request, 'sacco/reg/edit-registration.html', context) """
       
        registration.shares_entrance_fee = shares_entrance_fee
        registration.shares_application_fee = shares_application_fee
        registration.savings_entrance_fee = savings_entrance_fee
        registration.updated_on = timezone.now()
        registration.updated_by = request.user
        registration.save()
    

        # saving the expense in the database after creating it
        messages.success(request, SUCCESS_FEE_SAVED)

        # redirect to the expense page to see the expenses
        return redirect('registration')

@login_required(login_url='sign-in')
def registration_reciept(request, id):
    r = Registration.objects.get(pk=id)
    context = { 'r' : r}
    return render(request, 'sacco/reciept/r1.html', context)

""" Loans """
@login_required(login_url='sign-in')
def loan(request):
    registration = Loan.objects.filter(is_paid=0)
    context = { 'registration' : registration}
    return render(request, 'sacco/loan/loan.html', context)

@login_required(login_url='sign-in')
def loan_info(request, id):
    loan = Loan.objects.get(pk=id)
    context = { 'loan' : loan }
    return render(request, 'sacco/loan/loan-info.html', context)

@login_required(login_url='sign-in')
def add_loan(request):
    members = LoanFee.objects.filter(is_issued=0)
    # members = User.objects.filter(groups=group)
    try: 
        st = Settings.objects.get(pk=1)
    except Settings.DoesNotExist:
        pass

    context = {'values': request.POST, 'members' : members, 'st' : st }

    print(request.POST)

    if request.method == 'GET':
        if members:
            return render(request, 'sacco/loan/add-loan.html', context)
        else:
            messages.error(request,  ERROR_LOAN_FEE)
            return render(request, 'sacco/error.html')

    # The view to handle the form POST requests
    if request.method == 'POST':
      
        amount = request.POST['amount']

        if not amount:
            messages.error(request, ERROR_AMOUNT)
            return render(request, 'sacco/loan/add-loan.html', context)
        
        status = request.POST['status']
        print(status)

        if not status:
            messages.error(request, "Status is required")
            return render(request, 'sacco/loan/add-loan.html', context)

        
        if int(amount) < int(MIN_LOAN):
            messages.error(request, ERROR_MIN_LOAN)
            return render(request, 'sacco/loan/add-loan.html', context)
        
        if int(amount) > int(MAX_LOAN):
            messages.error(request, ERROR_MAX_LOAN)
            return render(request, 'sacco/loan/add-loan.html', context)

        
        duration = request.POST['duration']

        if not duration:
            messages.error(request, LOAN_DURATION)
            return render(request, 'sacco/loan/add-loan.html', context)
        else:
            due_date = add_months(int(duration))

        interest = request.POST['interest']

        if not interest:
            messages.error(request, LOAN_INTEREST_REQ)
            return render(request, 'sacco/loan/add-loan.html', context)

        total_interest =    (float(amount) * (float(INTEREST) / 100)) * float(duration)
        # form_interest = float(interest) * float(duration)
        form_interest = float(interest)

        print('Form : ' + str(form_interest ))
        print('total : ' + str(total_interest))
        if  form_interest != total_interest:
            messages.error(request, LOAN_INTEREST_CALC)
            return render(request, 'sacco/loan/add-loan.html', context)
        
        insurance = request.POST['insurance']

        if not insurance:
            messages.error(request, LOAN_INSURANCE_REQ)
            return render(request, 'sacco/loan/add-loan.html', context)
        
        total_insurance = float(amount) * (float(INSUARANCE) / 100)

        if  float(insurance) != total_insurance:
            messages.error(request, LOAN_INSURANCE_CALC)
            return render(request, 'sacco/loan/add-loan.html', context)

        total = float(amount) + float(total_interest) + float(total_insurance)
        

        member = LoanFee.objects.get(id=request.POST.get('member'))

        if not member:
            messages.error(request, ERROR_AMOUNT)
            return render(request, 'sacco/loan/add-loan.html', context)

        

        
        Loan.objects.create( 
            loan_fees=member, 
            amount=amount, 
            interest_rate=INTEREST ,
            interest=total_interest,
            insuarance_rate=INSUARANCE, 
            insurance=total_insurance,
            due_date=due_date, 
            balance=total,
            months=duration,
            total=total, 
            is_paid = 0,
            status = status,
            created_by=request.user)

        messages.success(request, SUCCESS_FEE_SAVED)

        return redirect('loan')
    
@login_required(login_url='sign-in')
def edit_loan(request, id):
    try:
        l = Loan.objects.get(pk=id)
        st = Settings.objects.get(pk=1)
    except Loan.DoesNotExist:
        messages.error(request, ERROR_404)
        return render(request, 'sacco/error.html')
    
    p = Payments.objects.filter(loan=id)

    print(request.POST)

    context = {
        'values': l, 
        'l' : l,
        'st' : st
    }

    if p:
        messages.error(request,  ERROR_LOAN_EDIT)
        return render(request, 'sacco/error.html', context)

    if request.method == 'GET':
         return render(request, 'sacco/loan/edit-loan.html', context)

    # The view to handle the form POST requests
    if request.method == 'POST':
      
        amount = request.POST['amount']

        if not amount:
            messages.error(request, ERROR_AMOUNT)
            return render(request, 'sacco/loan/edit-loan.html', context)
    
        status = request.POST['status']

        if not status:
            messages.error(request, "Status is required")
            return render(request, 'sacco/loan/edit-loan.html', context)
        
        
        if int(float(amount)) < int(MIN_LOAN):
            messages.error(request, ERROR_MIN_LOAN)
            return render(request, 'sacco/loan/edit-loan.html', context)
        
        if int(float(amount)) > int(MAX_LOAN):
            messages.error(request, ERROR_MAX_LOAN)
            return render(request, 'sacco/loan/edit-loan.html', context)
        
        duration = request.POST['duration']

        if not duration:
            messages.error(request, LOAN_DURATION)
            return render(request, 'sacco/loan/edit-loan.html', context)
        else:
            due_date = add_months(int(duration))

        interest = (float(amount) * (float(INTEREST) / 100)) * float(duration)

        fines = request.POST['fine']
        if not fines:
            fines = 0


    
        
        insurance = float(amount) * (float(INSUARANCE) / 100)

    

        total = float(amount) + float(interest) + float(insurance) + float(fines)
        

        member = User.objects.get(id=request.POST.get('member'))

        if not member:
            messages.error(request, ERROR_AMOUNT)
            return render(request, 'sacco/loan/edit-loan.html', context)


        
       
        
        l.member=member
        l.amount=amount 
        l.interest_rate=INTEREST
        l.interest=interest
        l.insuarance_rate=INSUARANCE
        l.insurance=insurance
        l.due_date=due_date 
        l.balance=total
        l.months=duration
        l.total=total
        l.fines=fines
        l.status = status
        l.updated_by = request.user
        l.updated_on = timezone.now()
        l.save()
    

        # saving the expense in the database after creating it
        messages.success(request, 'Loan Fee updated successfully')

        # redirect to the expense page to see the expenses
        return redirect('loan')
    
@login_required(login_url='sign-in')
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
        elif(float(paid_amount) > float(loan.balance)):
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


@login_required(login_url='sign-in')
def paid_loan(request):
    registration = Loan.objects.filter(is_paid=1)
    context = { 'registration' : registration}
    return render(request, 'sacco/loan/loan.html', context)
@login_required(login_url='sign-in')
def unpaid_loan(request):
    registration = Loan.objects.filter(is_paid=0)
    context = { 'registration' : registration}
    return render(request, 'sacco/loan/loan.html', context)



""" Capital Shares """
@login_required(login_url='sign-in')
def capital_shares(request):
    users = User.objects.filter(Q(groups=group)).prefetch_related('groups')
  
    if request.method == 'GET':

        registration = CapitalShares.objects.all()
        context = { 'registration' : registration, 'users' : users} 
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
                return render(request, 'sacco/registration/registration.html', context)
            else:
                registration = CapitalShares.objects.filter(created_on__range=(start_date, end_date), member=user)
               
                
                context = { 
                    'registration' : registration,
                  
                    'users': users,
                    'values' : request.POST
                    }
                return render(request, 'sacco/registration/registration.html', context)

        return render(request, 'sacco/registration/registration.html', context)


@login_required(login_url='sign-in')
def add_capital_shares(request):
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
            messages.error(request, 'Amount is required')
            return render(request, 'sacco/registration/add-registration.html', context)

        if int(amount) != CAPITAL_SHARE:
            messages.error(request, ERROR_INC_AMOUNT + str(CAPITAL_SHARE))
            return render(request, 'sacco/registration/add-registration.html', context)


        member = User.objects.get(id=request.POST.get('member'))

        if not member:
            messages.error(request, ERROR_REG_MEMBER)
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
            messages.error(request, str(calendar.month_abbr[current_month])  + ERROR_CS_MONTH_PAYMENT)
            return render(request, 'sacco/registration/add-registration.html', context)
       
        # if no error we save the data into database
        # we use the expense model
        # create the expense
        CapitalShares.objects.create( member=member, amount=amount, created_by=request.user)

        # saving the expense in the database after creating it
        messages.success(request, 'Capital Shares Fee saved successfully')

        # redirect to the expense page to see the expenses
        return redirect('capital-shares')
    

@login_required(login_url='sign-in')
def edit_capital_shares(request, id):
    try:
        registration = CapitalShares.objects.get(pk=id)
    except CapitalShares.DoesNotExist:
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
        
        if float(amount) != float(CAPITAL_SHARE):
            messages.error(request, 'Amount should be ' + str(CAPITAL_SHARE))
            return render(request, 'sacco/registration/edit-registration.html', context)
       
        registration.amount = amount
        registration.updated_by = request.user
        registration.updated_on = timezone.now()
        registration.save()
    

        # saving the expense in the database after creating it
        messages.success(request, SUCCESS_FEE_SAVED)

        # redirect to the expense page to see the expenses
        return redirect('capital-shares')

@login_required(login_url='sign-in')
def capitalshare_reciept(request, id):
    r = CapitalShares.objects.get(pk=id)
    context = { 'r' : r}
    return render(request, 'sacco/reciept/r1.html', context)

"""  Shares """
@login_required(login_url='sign-in')
def shares(request):
    users = User.objects.filter(Q(groups=group)).prefetch_related('groups')
  
    if request.method == 'GET':

        registration = Shares.objects.all()
        context = { 'registration' : registration, 'users' : users} 
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
                return render(request, 'sacco/registration/registration.html', context)
            else:
                registration = Shares.objects.filter(created_on__range=(start_date, end_date), member=user)
               
                
                context = { 
                    'registration' : registration,
                  
                    'users': users,
                    'values' : request.POST
                    }
                return render(request, 'sacco/registration/registration.html', context)

        return render(request, 'sacco/registration/registration.html', context)
@login_required(login_url='sign-in')
def add_shares(request):
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
            messages.error(request,ERROR_AMOUNT)
            return render(request, 'sacco/registration/add-registration.html', context)

        if int(amount) < SHARES_MIN:
            messages.error(request, ERROR_SHARE_MIN + str(SHARES_MIN))
            return render(request, 'sacco/registration/add-registration.html', context)


        member = User.objects.get(id=request.POST.get('member'))

        if not member:
            messages.error(request, MEMBERS_EXIST)
            return render(request, 'sacco/registration/add-registration.html', context)
        
       
    
        Shares.objects.create( member=member, amount=amount, created_by=request.user)

        # saving the expense in the database after creating it
        messages.success(request, SUCCESS_FEE_SAVED)

        # redirect to the expense page to see the expenses
        return redirect('shares')
@login_required(login_url='sign-in')
def edit_shares(request, id):
    try:
        registration = Shares.objects.get(pk=id)
    except Shares.DoesNotExist:
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
        
        if float(amount) < float(SHARES_MIN):
            messages.error(request, ERROR_SHARE_MIN + str(SHARES_MIN))
            return render(request, 'sacco/registration/add-registration.html', context)

       
        registration.amount = amount
        registration.updated_by = request.user
        registration.updated_on = timezone.now()
        registration.save()
    

        # saving the expense in the database after creating it
        messages.success(request, SUCCESS_FEE_EDITED)

        # redirect to the expense page to see the expenses
        return redirect('shares')


@login_required(login_url='sign-in')
def shares_reciept(request, id):
    r = Shares.objects.get(pk=id)
    context = { 'r' : r}
    return render(request, 'sacco/reciept/r1.html', context)

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
                return render(request, 'sacco/nhif/nhif.html', context)
            else:
                registration = NHIF.objects.filter(created_on__range=(start_date, end_date), member=user)
               
                
                context = { 
                    'registration' : registration,
                  
                    'users': users,
                    'values' : request.POST
                    }
                return render(request, 'sacco/nhif/nhif.html', context)

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

""" Cheque """
@login_required(login_url='sign-in')
def cheque(request):
    users = User.objects.filter(Q(groups=group)).prefetch_related('groups')
  
    if request.method == 'GET':

        registration = Cheque.objects.all()
        context = { 'registration' : registration, 'users' : users} 
        return render(request, 'sacco/cheque/cheque.html', context)
   
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
                return render(request, 'sacco/cheque/cheque.html', context)
            else:
                registration = Cheque.objects.filter(created_on__range=(start_date, end_date), member=user)
               
                
                context = { 
                    'registration' : registration,
                  
                    'users': users,
                    'values' : request.POST
                    }
                return render(request, 'sacco/cheque/cheque.html', context)

        return render(request, 'sacco/cheque/cheque.html', context)
    

@login_required(login_url='sign-in')
def add_cheque(request):
    members = User.objects.filter(groups=group)

    context = {'values': request.POST, 'members' : members }

    print(request.POST)

    if request.method == 'GET':
        if members:
            return render(request, 'sacco/cheque/add-cheque.html', context)
        else:
            messages.error(request,  MEMBERS_EXIST)
            return render(request, 'sacco/error.html')

    # The view to handle the form POST requests
    if request.method == 'POST':
      
        amount = request.POST['amount']

        if not amount:
            messages.error(request, ERROR_AMOUNT)
            return render(request, 'sacco/cheque/add-cheque.html', context)

        commission = request.POST['commission']

        if not commission:
            messages.error(request, ERROR_AMOUNT)
            return render(request, 'sacco/cheque/add-cheque.html', context)


        member = User.objects.get(id=request.POST.get('member'))

        if not member:
            messages.error(request, ERROR_REG_MEMBER)
            return render(request, 'sacco/cheque/add-cheque.html', context)
       
        # if no error we save the data into database
        # we use the expense model
        # create the expense
        Cheque.objects.create( member=member, amount=amount, commission=commission, created_by=request.user)

        # saving the expense in the database after creating it
        messages.success(request, SUCCESS_FEE_SAVED)

        # redirect to the expense page to see the expenses
        return redirect('cheque')
@login_required(login_url='sign-in')
def edit_cheque(request, id):
    try:
        registration = Cheque.objects.get(pk=id)
    except Cheque.DoesNotExist:
        messages.error(request, ERROR_404)
        return render(request, 'sacco/error.html')

    context = {
        'values': registration, 
        'registration' : registration 
    }

    if request.method == 'GET':
        return render(request, 'sacco/cheque/edit-cheque.html', context)

    # The view to handle the form POST requests
    if request.method == 'POST':
      
        amount = request.POST['amount']

        if not amount:
            messages.error(request, ERROR_AMOUNT)
            return render(request, 'sacco/cheque/edit-cheque.html', context)
        
        commission = request.POST['commission']

        if not commission:
            messages.error(request, ERROR_AMOUNT)
            return render(request, 'sacco/cheque/add-cheque.html', context)

        registration.amount = amount
        registration.commission = commission
        registration.updated_by = request.user
        registration.updated_on = timezone.now()
        registration.save()
    

        # saving the expense in the database after creating it
        messages.success(request, SUCCESS_FEE_EDITED)

        # redirect to the expense page to see the expenses
        return redirect('cheque')
    
@login_required(login_url='sign-in')
def cheque_reciept(request, id):
    r = Cheque.objects.get(pk=id)
    context = { 'r' : r}
    return render(request, 'sacco/reciept/r1.html', context)

""" Account """
@login_required(login_url='sign-in')
def account(request):
    users = User.objects.filter(Q(groups=group)).prefetch_related('groups')
  
    if request.method == 'GET':

        registration = Account.objects.all()
        context = { 'registration' : registration, 'users' : users} 
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
                return render(request, 'sacco/registration/registration.html', context)
            else:
                registration = Account.objects.filter(created_on__range=(start_date, end_date), member=user)
               
                
                context = { 
                    'registration' : registration,
                  
                    'users': users,
                    'values' : request.POST
                    }
                return render(request, 'sacco/registration/registration.html', context)

        return render(request, 'sacco/registration/registration.html', context)
@login_required(login_url='sign-in')
def add_account(request):
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
        Account.objects.create( member=member, amount=amount, created_by=request.user)

        # saving the expense in the database after creating it
        messages.success(request, SUCCESS_FEE_SAVED)

        # redirect to the expense page to see the expenses
        return redirect('account')
@login_required(login_url='sign-in')
def edit_account(request, id):
    try:
        registration = Account.objects.get(pk=id)
    except Account.DoesNotExist:
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
def account_reciept(request, id):
    r = Account.objects.get(pk=id)
    context = { 'r' : r}
    return render(request, 'sacco/reciept/r1.html', context)


""" Passbook """
@login_required(login_url='sign-in')
def passbook(request):

    users = User.objects.filter(Q(groups=group)).prefetch_related('groups')
  
    if request.method == 'GET':

        registration = Passbook.objects.all()
        context = { 'registration' : registration, 'users' : users} 
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
                return render(request, 'sacco/registration/registration.html', context)
            else:
                registration = Passbook.objects.filter(created_on__range=(start_date, end_date), member=user)
               
                
                context = { 
                    'registration' : registration,
                  
                    'users': users,
                    'values' : request.POST
                    }
                return render(request, 'sacco/registration/registration.html', context)

        return render(request, 'sacco/registration/registration.html', context)
@login_required(login_url='sign-in')
def add_passbook(request):
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
            messages.error(request,  ERROR_AMOUNT)
            return render(request, 'sacco/registration/add-registration.html', context)

        if float(amount) != float(PASSBOOK):
            messages.error(request, ERROR_INC_AMOUNT + str(PASSBOOK))
            return render(request, 'sacco/registration/add-registration.html', context)


        member = User.objects.get(id=request.POST.get('member'))

        if not member:
            messages.error(request, ERROR_REG_MEMBER)
            return render(request, 'sacco/registration/add-registration.html', context)
       
        # if no error we save the data into database
        # we use the expense model
        # create the expense
        Passbook.objects.create( member=member, amount=amount, created_by=request.user)

        # saving the expense in the database after creating it
        messages.success(request, SUCCESS_FEE_SAVED)

        # redirect to the expense page to see the expenses
        return redirect('passbook')
@login_required(login_url='sign-in')
def edit_passbook(request, id):
    

    try:
        registration = Passbook.objects.get(pk=id)
    except Passbook.DoesNotExist:
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
        
        if float(amount) != float(PASSBOOK):
            messages.error(request, ERROR_INC_AMOUNT + str(PASSBOOK))
            return render(request, 'sacco/registration/add-registration.html', context)
       
        registration.amount = amount
        registration.updated_by = request.user
        registration.updated_on = timezone.now()
        registration.save()
    

        # saving the expense in the database after creating it
        messages.success(request, SUCCESS_FEE_EDITED)

        # redirect to the expense page to see the expenses
        return redirect('passbook')


@login_required(login_url='sign-in')
def passbook_reciept(request, id):
    r = Passbook.objects.get(pk=id)
    context = { 'r' : r}
    return render(request, 'sacco/reciept/r1.html', context)
    

@login_required(login_url='sign-in')
def settings(request):
    try:
        values = Settings.objects.get(pk=1)

        print(request.POST)

        context = {'values' : values }
        
        if request.method == 'GET':
            return render(request, 'sacco/settings.html', context)

        if request.method == 'POST':
            SHARES_ENTRANCE_FEE = request.POST['SHARES_ENTRANCE_FEE']
            SHARES_APPLICATION_FEE = request.POST['SHARES_APPLICATION_FEE']
            SAVINGS_ENTRANCE_FEE = request.POST['SAVINGS_ENTRANCE_FEE']
            MIN_LOAN = request.POST['MIN_LOAN']
            MAX_LOAN = request.POST['MAX_LOAN']
            CAPITAL_SHARE = request.POST['CAPITAL_SHARE']
            SHARES_MIN = request.POST['SHARES_MIN']
            ACCOUNT = request.POST['ACCOUNT']
            ACCOUNT_WITHDRAWAL = request.POST['ACCOUNT_WITHDRAWAL']
            PROCESSING_FEE = request.POST['PROCESSING_FEE']
            PASSBOOK = request.POST['PASSBOOK']
            INTEREST = request.POST['INTEREST']
            INSUARANCE = request.POST['INSUARANCE']
            PHONE_NUMBER = request.POST['PHONE_NUMBER']
    


            values.SHARES_ENTRANCE_FEE=SHARES_ENTRANCE_FEE
            values.SHARES_APPLICATION_FEE=SHARES_APPLICATION_FEE
            values.SAVINGS_ENTRANCE_FEE=SAVINGS_ENTRANCE_FEE
            values.MIN_LOAN=MIN_LOAN
            values.MAX_LOAN=MAX_LOAN 
            values.CAPITAL_SHARE=CAPITAL_SHARE 
            values.SHARES_MIN=SHARES_MIN
            values.ACCOUNT=ACCOUNT
            values.ACCOUNT_WITHDRAWAL=ACCOUNT_WITHDRAWAL
            values.PROCESSING_FEE=PROCESSING_FEE
            values.PASSBOOK=PASSBOOK
            values.INTEREST=INTEREST 
            values.INSUARANCE=INSUARANCE 
            values.PHONE_NUMBER=PHONE_NUMBER
            values.created_by=request.user
            values.save()


            messages.success(request, 'Settings updated successfully')
        
            logout(request)
            return redirect('sign-in')
        
    except Settings.DoesNotExist:
        Settings.objects.create(
            SHARES_ENTRANCE_FEE = 0,
            SHARES_APPLICATION_FEE = 0,
            SAVINGS_ENTRANCE_FEE = 0,
            MIN_LOAN = 0,
            MAX_LOAN = 0,
            CAPITAL_SHARE = 0,
            SHARES_MIN = 0,
            ACCOUNT = 0,
            ACCOUNT_WITHDRAWAL = 0,
            PROCESSING_FEE = 0,
            PASSBOOK = 0,
            INTEREST = 0,
            INSUARANCE = 0,
            PHONE_NUMBER = 0,
            SACCO_PHONE_NUMBER = 0,
            created_by=request.user           

        )

        messages.success(request, 'Settings created  successfully')
        
        logout(request)
        return redirect('sign-in')

""" Loan Fee """
@login_required(login_url='sign-in')
def loan_fee(request):

    users = User.objects.filter(Q(groups=group)).prefetch_related('groups')
  
    if request.method == 'GET':

        registration = LoanFee.objects.all()
        context = { 'registration' : registration, 'users' : users} 
        return render(request, 'sacco/loan_fee/loan-fee.html', context)
   
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
                return render(request, 'sacco/loan_fee/loan-fee.html', context)
            else:
                registration = LoanFee.objects.filter(created_on__range=(start_date, end_date), member=user)
               
                
                context = { 
                    'registration' : registration,
                  
                    'users': users,
                    'values' : request.POST
                    }
                return render(request, 'sacco/loan_fee/loan-fee.html', context)

        return render(request, 'sacco/registration/registration.html', context)

@login_required(login_url='sign-in')
def add_loan_fee(request):
    
        members = User.objects.filter(groups=group)
    
        context = {'values': request.POST, 'members' : members }

        print(request.POST)

        if request.method == 'GET':
            if members:
                return render(request, 'sacco/loan_fee/add-loan-fee.html', context)
            else:
                messages.error(request,  MEMBERS_EXIST)
                return render(request, 'sacco/loan_fee/add-loan-fee.html', context)

        # The view to handle the form POST requests
        if request.method == 'POST':
        
            loan_fee = request.POST['loan_fee']
            if not loan_fee:
                messages.error(request, ERROR_AMOUNT)
                return render(request, 'sacco/loan_fee/add-loan-fee.html', context)


            member = User.objects.get(id=request.POST.get('member'))
            if not member:
                messages.error(request, ERROR_REG_MEMBER)
                return render(request, 'sacco/loan_fee/add-loan-fee.html', context)
            
            processing = request.POST['processing']
            if not processing:
                messages.error(request, ERROR_AMOUNT)
                return render(request, 'sacco/loan_fee/add-loan-fee.html', context)
            
            
        
    
            LoanFee.objects.create( 
                member=member, 
                loan_fee=loan_fee, 
                processing=processing,
                created_by=request.user)

            
            messages.success(request, SUCCESS_FEE_SAVED)

            
            return redirect('loan-fee')

@login_required(login_url='sign-in')
def edit_loan_fee(request, id):
    try:
        registration = LoanFee.objects.get(pk=id)
    except LoanFee.DoesNotExist:
        messages.error(request, ERROR_404)
        return render(request, 'sacco/error.html')

    next_page = request.GET.get('nxt')

    context = {
        'values': registration, 
        'registration' : registration,
        'next_page' : next_page
    }

    
    
    if request.method == 'GET':
        return render(request, 'sacco/loan_fee/edit-loan-fee.html', context)

    # The view to handle the form POST requests
    if request.method == 'POST':
      
        loan_fee = request.POST['loan_fee']

        if not loan_fee:
            messages.error(request, ERROR_AMOUNT)
            return render(request, 'sacco/loan_fee/edit-loan-fee.html', context)
        
        processing = request.POST['processing']
        if not processing:
            messages.error(request, ERROR_AMOUNT)
            return render(request, 'sacco/loan_fee/edit-loan-fee.html', context)
        
       
        if next_page:
            registration.loan_fee = loan_fee
            registration.processing = processing
            registration.updated_by = request.user
            registration.updated_on = timezone.now()
            registration.save()
        

            # saving the expense in the database after creating it
            messages.success(request, SUCCESS_FEE_EDITED)

            # redirect to the expense page to see the expenses
            return redirect('nhif' )
        else:
            registration.loan_fee = loan_fee
            registration.processing = processing
            registration.updated_by = request.user
            registration.updated_on = timezone.now()
            registration.save()
        

            # saving the expense in the database after creating it
            messages.success(request, SUCCESS_FEE_EDITED)

            # redirect to the expense page to see the expenses
            return redirect('loan-fee' )


@login_required(login_url='sign-in')
def loanfee_reciept(request, id):
    r = LoanFee.objects.get(pk=id)
    context = { 'r' : r}
    return render(request, 'sacco/reciept/r1.html', context)

@login_required(login_url='sign-in')
def payments(request):
    r = Payments.objects.all()
    context = { 'r' : r}
    return render(request, 'sacco/loan/payments.html', context)

@login_required(login_url='sign-in')
def payments_reciept(request, id):
    r = Payments.objects.get(pk=id)
    context = { 'r' : r}
    return render(request, 'sacco/reciept/r1.html', context)
































































