# Generated by Django 4.1.4 on 2023-04-18 19:34

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_counter_t_loan_alter_account_transaction_id_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Counter',
        ),
        migrations.AlterField(
            model_name='account',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('10ccbde2-292c-419b-b157-b4649ae2c76a'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='capitalshares',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('eac1d6ff-66d3-4d38-a7ae-af4d6a0885fb'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='cheque',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('decfdd32-4ac5-4e00-bf2f-52551bd5522d'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='loan',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('4e7b52f8-65cd-49bc-ba3d-79a64a7c2c2a'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='loanfee',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('4ebd2a1f-5211-4280-9615-a81deda4bb51'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='nhif',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('8862d0a5-534c-48b2-98de-b86c815aa57d'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='passbook',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('5a706c70-2bba-4e4e-bf25-eb9bdecbc613'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='payments',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('0ea9d002-69d7-466d-8dba-42c29d8be112'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='registration',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('430df225-b68a-4976-82d7-77a4416c2700'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='shares',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('a96fd9c6-4f22-4a37-afa6-6bdc3c8a3a39'), max_length=200, unique=True),
        ),
    ]
