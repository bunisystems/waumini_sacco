from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models.deletion import CASCADE
from django.db.models.expressions import OrderBy
from sacco.functions import *
from django.dispatch import receiver
from django.db.models.signals import post_save



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    member_no_shares = models.CharField(max_length=200, unique=True, null=True)
    member_no_savings = models.CharField(max_length=200, unique=True, null=True)
    id_no = models.CharField(max_length=200, unique=True, null=True)

    def __str__(self):
        return self.user.username
        
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


class Registration(models.Model):
    reg_no = models.CharField(max_length=200, unique=True)
    transaction_id = models.CharField(max_length=200, unique=True, default=generate_transaction_uuid())
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name="member_registration")

    shares_entrance_fee = models.DecimalField(max_digits=8, decimal_places=2)
    shares_application_fee = models.DecimalField(max_digits=8, decimal_places=2)
    savings_entrance_fee = models.DecimalField(max_digits=8, decimal_places=2)

    is_deleted = models.BooleanField(default=0)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reg_created_by")
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reg_updated_by", null=True, blank=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reg_deleted_by", null=True, blank=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(null=True)
    deleted_on = models.DateTimeField(null=True)
    
    def __str__(self):
        return self.member
    
    def save(self, *args, **kwargs):
        reg_id = self.id
        if Registration.objects.filter(id=reg_id).exists():
            super(Registration, self).save()
        else:
            current_time = datetime.now()
            self.reg_no = 'WRG' + current_time.strftime("%Y%m%d%H%M%S")
            self.transaction_id = generate_transaction_uuid()
            super().save(*args, **kwargs)

class LoanFee(models.Model):
    loan_fee_no = models.CharField(max_length=200, unique=True)
    transaction_id = models.CharField(max_length=200, unique=True, default=generate_transaction_uuid())
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name="member_loan_fee")
    loan_fee = models.DecimalField(max_digits=8, decimal_places=2)
    processing = models.DecimalField(max_digits=8, decimal_places=2)
    
    is_deleted = models.BooleanField(default=0)
    is_issued = models.BooleanField(default=0)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="loan_fee_updated_by", null=True, blank=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="loan_fee_deleted_by", null=True, blank=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(null=True)
    deleted_on = models.DateTimeField(null=True)
    
    def __str__(self):
        return self.member
    
    def save(self, *args, **kwargs):
        loan_fee_no = self.id
        if LoanFee.objects.filter(id=loan_fee_no).exists():
            super(LoanFee, self).save()
        else:
            current_time = datetime.now()
            self.loan_fee_no = 'WLF' + current_time.strftime("%Y%m%d%H%M%S")
            self.transaction_id = generate_transaction_uuid()
            super().save(*args, **kwargs)

class Loan(models.Model):

    loan_no = models.CharField(max_length=200, unique=True)
    loan_fees = models.ForeignKey(LoanFee, on_delete=models.CASCADE, related_name="member_loan_fee")
    transaction_id = models.CharField(max_length=200, unique=True, default=generate_transaction_uuid())
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    interest_rate = models.IntegerField ()
    interest = models.DecimalField(max_digits=8, decimal_places=2)
    insuarance_rate = models.IntegerField()
    insurance = models.DecimalField(max_digits=8, decimal_places=2)
    fines = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    balance = models.DecimalField(max_digits=8, decimal_places=2)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    is_paid = models.BooleanField(default=0)
    status = models.CharField(max_length=200)
    months = models.IntegerField()
    due_date = models.DateTimeField()

    is_deleted = models.BooleanField(default=0)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="loan_created_by",)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="loan_updated_by", null=True, blank=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="loan_deleted_by", null=True, blank=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(null=True)
    deleted_on = models.DateTimeField(null=True)
    
    def __str__(self):
        return self.loan_no
    
    def save(self, *args, **kwargs):        
        loan_id = self.id
        if Loan.objects.filter(id=loan_id).exists():
            super(Loan, self).save()
        else:
            current_time = datetime.now()
            self.loan_no = 'WLN' + current_time.strftime("%Y%m%d%H%M%S")
            self.transaction_id = generate_transaction_uuid()
            loan_fees = self.loan_fees
            loan_fees.is_issued = 1
            loan_fees.save()
            super().save(*args, **kwargs)

# Payments
class Payments(models.Model):

    payment_no = models.CharField(max_length=200, unique=True)
    transaction_id = models.CharField(max_length=200, unique=True, default=generate_transaction_uuid())
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)

    total = models.DecimalField(max_digits=8, decimal_places=2)
    balance = models.DecimalField(max_digits=8, decimal_places=2)
    paid = models.DecimalField(max_digits=8, decimal_places=2)
    unpaid = models.DecimalField(max_digits=8, decimal_places=2)
		
    is_deleted = models.BooleanField(default=0)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(null=True)
    deleted_on = models.DateTimeField(null=True)


    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments_created_by", null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments_updated_by", null=True, blank=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments_deleted_by", null=True, blank=True)

	
    
    def save(self, *args, **kwargs):
        current_time = datetime.now()
        self.payment_no = 'WPY' + current_time.strftime("%Y%m%d%H%M%S")
        self.transaction_id = generate_transaction_uuid()
        self.unpaid = self.balance - self.paid
        super().save(*args, **kwargs)

        loan = self.loan   # fetch the related A object in my_a
        loan.balance = self.unpaid # update the no field of that object

        if loan.balance == 0:
            loan.is_paid = 1
            loan.save()

        loan.save()     # save the update to the database

        self.save_balance()


    def save_balance(self):
        balance = Balance.objects.create(
        loan = self.loan,
        amount = self.unpaid)

# Balance		
class Balance(models.Model):

	loan =  models.ForeignKey(Loan, on_delete=models.CASCADE, related_name="balance_loan")
	amount = models.DecimalField(max_digits=8, decimal_places=2)

	def __str__(self):
		return str(self.amount)


class CapitalShares(models.Model):
    c_share_no = models.CharField(max_length=200, unique=True)
    transaction_id = models.CharField(max_length=200, unique=True, default=generate_transaction_uuid())
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name="member_capital_shares")
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    is_deleted = models.BooleanField(default=0)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(null=True)
    deleted_on = models.DateTimeField(null=True)


    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="capital_shares_created_by", null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="capital_shares_updated_by", null=True, blank=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="capital_shares_deleted_by", null=True, blank=True)
    
    def __str__(self):
        return self.member


    def save(self, *args, **kwargs):
        capitalshare_id = self.id
        if CapitalShares.objects.filter(id=capitalshare_id).exists():
            super(CapitalShares, self).save()
        else:
            current_time = datetime.now()
            self.c_share_no = 'WCS' + current_time.strftime("%Y%m%d%H%M%S")
            self.transaction_id = generate_transaction_uuid()
            super().save(*args, **kwargs)

class Shares(models.Model):
    share_no = models.CharField(max_length=200, unique=True)
    transaction_id = models.CharField(max_length=200, unique=True, default=generate_transaction_uuid())
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name="member_shares")
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    is_deleted = models.BooleanField(default=0)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(null=True)
    deleted_on = models.DateTimeField(null=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shares_created_by", null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shares_updated_by", null=True, blank=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shares_deleted_by", null=True, blank=True)
    
    def __str__(self):
        return self.member

    def save(self, *args, **kwargs):
        share_id = self.id
        if Shares.objects.filter(id=share_id).exists():
            super(Shares, self).save()
        else:
            current_time = datetime.now()
            self.share_no = 'WSH' + current_time.strftime("%Y%m%d%H%M%S")
            self.transaction_id = generate_transaction_uuid()
            super().save(*args, **kwargs)

class NHIF(models.Model):
    nhif_no = models.CharField(max_length=200, unique=True)
    transaction_id = models.CharField(max_length=200, unique=True, default=generate_transaction_uuid())
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name="member_nhif")
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    commission = models.DecimalField(max_digits=8, decimal_places=2)
    
    is_deleted = models.BooleanField(default=0)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="nhif_updated_by", null=True, blank=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="nhif_deleted_by", null=True, blank=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(null=True)
    deleted_on = models.DateTimeField(null=True)
    
    def __str__(self):
        return self.member
    
    def save(self, *args, **kwargs):
        nhif_id = self.id
        if NHIF.objects.filter(id=nhif_id).exists():
            super(NHIF, self).save()
        else:
            current_time = datetime.now()
            self.nhif_no = 'WNH' + current_time.strftime("%Y%m%d%H%M%S")
            self.transaction_id = generate_transaction_uuid()
            super().save(*args, **kwargs)

class Cheque(models.Model):
    cheque_no = models.CharField(max_length=200, unique=True)
    transaction_id = models.CharField(max_length=200, unique=True, default=generate_transaction_uuid())
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name="member_cheque")
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    commission = models.DecimalField(max_digits=8, decimal_places=2)
    is_deleted = models.BooleanField(default=0)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cheque_updated_by", null=True, blank=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cheque_deleted_by", null=True, blank=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(null=True)
    deleted_on = models.DateTimeField(null=True)
    
    def __str__(self):
        return self.member
    
    def save(self, *args, **kwargs):
        cheque_id = self.id
        if Cheque.objects.filter(id=cheque_id).exists():
            super(Cheque, self).save()
        else:
            current_time = datetime.now()
            self.cheque_no = 'WCH' + current_time.strftime("%Y%m%d%H%M%S")
            self.transaction_id = generate_transaction_uuid()
            super().save(*args, **kwargs)

class Account(models.Model):
    account_no = models.CharField(max_length=200, unique=True)
    transaction_id = models.CharField(max_length=200, unique=True, default=generate_transaction_uuid())
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name="member_account")
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    is_deleted = models.BooleanField(default=0)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="account_updated_by", null=True, blank=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="account_deleted_by", null=True, blank=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(null=True)
    deleted_on = models.DateTimeField(null=True)
    
    def __str__(self):
        return self.member
    
    def save(self, *args, **kwargs):
        account_id = self.id
        if Account.objects.filter(id=account_id).exists():
            super(Account, self).save()
        else:
            current_time = datetime.now()
            self.account_no = 'WAC' + current_time.strftime("%Y%m%d%H%M%S")
            self.transaction_id = generate_transaction_uuid()
            super().save(*args, **kwargs)


class Passbook(models.Model):
    passbook_no = models.CharField(max_length=200, unique=True)
    transaction_id = models.CharField(max_length=200, unique=True, default=generate_transaction_uuid())
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name="member_passbook")
    amount = models.DecimalField(max_digits=8, decimal_places=2)

    is_deleted = models.BooleanField(default=0)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="passbook_updated_by", null=True, blank=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="passbook_deleted_by", null=True, blank=True)


    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(null=True)
    deleted_on = models.DateTimeField(null=True)
    
    def __str__(self):
        return self.member
    
    def save(self, *args, **kwargs):
        passbook_no = self.id
        if Passbook.objects.filter(id=passbook_no).exists():
            super(Passbook, self).save()
        else:
            current_time = datetime.now()
            self.passbook_no = 'WPB' + current_time.strftime("%Y%m%d%H%M%S")
            self.transaction_id = generate_transaction_uuid()
            super().save(*args, **kwargs)
    

class Settings(models.Model):
    
    SHARES_ENTRANCE_FEE = models.IntegerField(null=True, blank=True)
    SHARES_APPLICATION_FEE = models.IntegerField(null=True, blank=True)
    SAVINGS_ENTRANCE_FEE = models.IntegerField(null=True, blank=True)
    MIN_LOAN = models.IntegerField(null=True, blank=True) 
    MAX_LOAN = models.IntegerField(null=True, blank=True)
    CAPITAL_SHARE = models.IntegerField(null=True, blank=True)
    SHARES_MIN = models.IntegerField(null=True, blank=True)
    ACCOUNT = models.IntegerField(null=True, blank=True)
    ACCOUNT_WITHDRAWAL = models.IntegerField(null=True, blank=True)
    PROCESSING_FEE = models.IntegerField(null=True, blank=True)
    PASSBOOK = models.IntegerField(null=True, blank=True)
    INTEREST = models.IntegerField(null=True, blank=True)
    INSUARANCE = models.IntegerField(null=True, blank=True)
    PHONE_NUMBER = models.IntegerField(null=True, blank=True)
    SACCO_PHONE_NUMBER = models.TextField(null=True, blank=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="settings_updated_by", null=True, blank=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="settings_deleted_by", null=True, blank=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(null=True)
    deleted_on = models.DateTimeField(null=True)






