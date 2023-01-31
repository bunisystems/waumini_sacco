# Generated by Django 4.1.4 on 2023-01-31 07:19

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_account_transaction_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('ef4ab7da-a003-4b9f-b8a8-2f8244e7d7b7'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='capitalshares',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('518d366f-b57c-4632-88ca-2223b32e671a'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='cheque',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('53746a4f-3849-4e4b-85ef-c735a73b7d70'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='loan',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('b8dc9bb5-308a-4a00-96ab-51c5eab27e73'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='nhif',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('4ff14084-3bca-4d4b-9b9b-99c60a83836c'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='passbook',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('d7944de0-7c98-472e-b967-48a15745f80b'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='payments',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('8f249808-13b2-415d-851e-e0a63a902ed8'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='processing',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('1586b1a0-e298-4fbb-b643-a6457a09aa61'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='registration',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('f4f3c870-f118-4cbd-91cd-6f3360ed4b45'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='shares',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('ab0a2e14-85f8-42c9-96b6-aacb3bc909a6'), max_length=200, unique=True),
        ),
    ]