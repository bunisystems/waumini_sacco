from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from sacco.functions import generate_transaction_uuid
from api.models import Statement
from decimal import Decimal

class Account_Deposit(models.Model):
    
    transaction_id = models.CharField(max_length=200, unique=True, default=generate_transaction_uuid())
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name="member_account_deposit")
    amount = models.DecimalField(max_digits=8, decimal_places=2)

    is_deleted = models.BooleanField(default=0)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="account_account_deposit_updated_by", null=True, blank=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="account_account_deposit_deleted_by", null=True, blank=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(null=True)
    deleted_on = models.DateTimeField(null=True)
    
    def __str__(self):
        return self.member
    
    def save(self, *args, **kwargs):
        account_id = self.id
        
        if Account_Deposit.objects.filter(id=account_id).exists():
            super(Account_Deposit, self).save()
        else:
            self.transaction_id = generate_transaction_uuid()
            last_statement = Statement.objects.filter(member=self.member).order_by('-created_on').first()
            
            if last_statement:
                # Create a new statement
            
                money_in = Decimal(str(self.amount))
                money_out = Decimal('0')
                balance = Decimal(str(self.amount)) + last_statement.balance
                Statement.objects.create(member=self.member, money_in=money_in, money_out=money_out, balance=balance, transaction_id=self.transaction_id)
            else:
                # Create a new statement
                
                money_in = self.amount
                money_out = 0
                balance = self.amount
                Statement.objects.create(member=self.member, money_in=money_in, money_out=money_out, balance=balance, transaction_id=self.transaction_id)            
            super().save(*args, **kwargs)