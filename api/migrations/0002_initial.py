# Generated by Django 4.1.4 on 2023-03-15 20:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loan_no', models.CharField(max_length=200, unique=True)),
                ('transaction_id', models.CharField(default=uuid.UUID('b2c77c72-042e-4b5d-874a-e649ee8ff968'), max_length=200, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('interest_rate', models.IntegerField()),
                ('interest', models.DecimalField(decimal_places=2, max_digits=8)),
                ('insuarance_rate', models.IntegerField()),
                ('insurance', models.DecimalField(decimal_places=2, max_digits=8)),
                ('fines', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=8)),
                ('total', models.DecimalField(decimal_places=2, max_digits=8)),
                ('is_paid', models.BooleanField(default=0)),
                ('status', models.CharField(max_length=200)),
                ('months', models.IntegerField()),
                ('due_date', models.DateTimeField()),
                ('is_deleted', models.BooleanField(default=0)),
                ('created_on', models.DateTimeField()),
                ('updated_on', models.DateTimeField(null=True)),
                ('deleted_on', models.DateTimeField(null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loan_created_by', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='loan_deleted_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member_no_shares', models.CharField(blank=True, max_length=200, null=True, unique=True)),
                ('member_no_savings', models.CharField(blank=True, max_length=200, null=True, unique=True)),
                ('id_no', models.CharField(blank=True, max_length=200, null=True, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Shares',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('share_no', models.CharField(max_length=200, unique=True)),
                ('transaction_id', models.CharField(default=uuid.UUID('3f55850e-0241-48b4-98f6-be1892961f2f'), max_length=200, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('is_deleted', models.BooleanField(default=0)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(null=True)),
                ('deleted_on', models.DateTimeField(null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shares_created_by', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shares_deleted_by', to=settings.AUTH_USER_MODEL)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member_shares', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shares_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SHARES_ENTRANCE_FEE', models.IntegerField(blank=True, null=True)),
                ('SHARES_APPLICATION_FEE', models.IntegerField(blank=True, null=True)),
                ('SAVINGS_ENTRANCE_FEE', models.IntegerField(blank=True, null=True)),
                ('MIN_LOAN', models.IntegerField(blank=True, null=True)),
                ('MAX_LOAN', models.IntegerField(blank=True, null=True)),
                ('CAPITAL_SHARE', models.IntegerField(blank=True, null=True)),
                ('SHARES_MIN', models.IntegerField(blank=True, null=True)),
                ('ACCOUNT', models.IntegerField(blank=True, null=True)),
                ('ACCOUNT_WITHDRAWAL', models.IntegerField(blank=True, null=True)),
                ('PROCESSING_FEE', models.IntegerField(blank=True, null=True)),
                ('PASSBOOK', models.IntegerField(blank=True, null=True)),
                ('INTEREST', models.IntegerField(blank=True, null=True)),
                ('INSUARANCE', models.IntegerField(blank=True, null=True)),
                ('PHONE_NUMBER', models.IntegerField(blank=True, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(null=True)),
                ('deleted_on', models.DateTimeField(null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='settings_deleted_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='settings_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reg_no', models.CharField(max_length=200, unique=True)),
                ('transaction_id', models.CharField(default=uuid.UUID('6d04d03b-251d-43d0-97e9-489b5cdc0d84'), max_length=200, unique=True)),
                ('shares_entrance_fee', models.DecimalField(decimal_places=2, max_digits=8)),
                ('shares_application_fee', models.DecimalField(decimal_places=2, max_digits=8)),
                ('savings_entrance_fee', models.DecimalField(decimal_places=2, max_digits=8)),
                ('is_deleted', models.BooleanField(default=0)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(null=True)),
                ('deleted_on', models.DateTimeField(null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reg_created_by', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reg_deleted_by', to=settings.AUTH_USER_MODEL)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member_registration', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reg_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_no', models.CharField(max_length=200, unique=True)),
                ('transaction_id', models.CharField(default=uuid.UUID('3275ea0a-b428-4832-8289-79ba73464126'), max_length=200, unique=True)),
                ('total', models.DecimalField(decimal_places=2, max_digits=8)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=8)),
                ('paid', models.DecimalField(decimal_places=2, max_digits=8)),
                ('unpaid', models.DecimalField(decimal_places=2, max_digits=8)),
                ('is_deleted', models.BooleanField(default=0)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(null=True)),
                ('deleted_on', models.DateTimeField(null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payments_created_by', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payments_deleted_by', to=settings.AUTH_USER_MODEL)),
                ('loan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.loan')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payments_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Passbook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passbook_no', models.CharField(max_length=200, unique=True)),
                ('transaction_id', models.CharField(default=uuid.UUID('b8791d0b-40a3-4a78-b4c4-d32d554e29a9'), max_length=200, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('is_deleted', models.BooleanField(default=0)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(null=True)),
                ('deleted_on', models.DateTimeField(null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='passbook_deleted_by', to=settings.AUTH_USER_MODEL)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member_passbook', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='passbook_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NHIF',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nhif_no', models.CharField(max_length=200, unique=True)),
                ('transaction_id', models.CharField(default=uuid.UUID('52c1c1ff-0565-4349-ba54-eeb7c00538dd'), max_length=200, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('commission', models.DecimalField(decimal_places=2, max_digits=8)),
                ('is_deleted', models.BooleanField(default=0)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(null=True)),
                ('deleted_on', models.DateTimeField(null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nhif_deleted_by', to=settings.AUTH_USER_MODEL)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member_nhif', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nhif_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LoanFee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loan_fee_no', models.CharField(max_length=200, unique=True)),
                ('transaction_id', models.CharField(default=uuid.UUID('473e5415-32f5-4b07-a2db-979ae96cb950'), max_length=200, unique=True)),
                ('loan_fee', models.DecimalField(decimal_places=2, max_digits=8)),
                ('processing', models.DecimalField(decimal_places=2, max_digits=8)),
                ('is_deleted', models.BooleanField(default=0)),
                ('is_issued', models.BooleanField(default=0)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(null=True)),
                ('deleted_on', models.DateTimeField(null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='loan_fee_deleted_by', to=settings.AUTH_USER_MODEL)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member_loan_fee', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='loan_fee_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='loan',
            name='loan_fees',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member_loan_fee', to='api.loanfee'),
        ),
        migrations.AddField(
            model_name='loan',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='loan_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Cheque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cheque_no', models.CharField(max_length=200, unique=True)),
                ('transaction_id', models.CharField(default=uuid.UUID('21141387-1d18-4b1f-a59a-75f56281c2ce'), max_length=200, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('commission', models.DecimalField(decimal_places=2, max_digits=8)),
                ('is_deleted', models.BooleanField(default=0)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(null=True)),
                ('deleted_on', models.DateTimeField(null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cheque_deleted_by', to=settings.AUTH_USER_MODEL)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member_cheque', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cheque_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CapitalShares',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_share_no', models.CharField(max_length=200, unique=True)),
                ('transaction_id', models.CharField(default=uuid.UUID('902ba56c-4e8b-4748-8a67-5dde89413437'), max_length=200, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('is_deleted', models.BooleanField(default=0)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(null=True)),
                ('deleted_on', models.DateTimeField(null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='capital_shares_created_by', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='capital_shares_deleted_by', to=settings.AUTH_USER_MODEL)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member_capital_shares', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='capital_shares_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('loan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='balance_loan', to='api.loan')),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_no', models.CharField(max_length=200, unique=True)),
                ('transaction_id', models.CharField(default=uuid.UUID('8dbd69ef-2ce6-4a0e-b274-dae0286183e1'), max_length=200, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('is_deleted', models.BooleanField(default=0)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(null=True)),
                ('deleted_on', models.DateTimeField(null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='account_deleted_by', to=settings.AUTH_USER_MODEL)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member_account', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='account_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]