# Generated by Django 4.1.4 on 2023-02-03 10:58

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_account_transaction_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('d577d286-391f-455d-b7a8-c98f0072bbde'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='capitalshares',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('743f9a93-7aab-4812-8d1e-f92679f308c6'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='cheque',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('3a63e4b6-8dd5-4bf4-8454-a0c0b3fe866a'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='loan',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('ac81268e-ab0a-4c21-88a3-ea2ff00ad831'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='nhif',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('30164121-3c51-467c-b8ea-6ad047dd7d69'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='passbook',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('5e2da9dd-a967-455f-a02c-f00dfa717792'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='payments',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('b77ac789-e750-40bd-9443-b81ecb1614e1'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='processing',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('dcec2f2b-710b-4d2a-a418-55bb74ab2668'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='registration',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('5d7b93c4-5b70-4c46-acab-8eb797518326'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='shares',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('8894d7b7-1704-4253-9045-7bc5eeb99e30'), max_length=200, unique=True),
        ),
    ]