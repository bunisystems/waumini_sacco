# Generated by Django 4.1.4 on 2023-02-18 17:03

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_alter_account_transaction_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('4ab6f9c4-deb7-4e91-9615-6610f4affbe5'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='capitalshares',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('511e867a-8163-4839-a432-2866e3b72450'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='cheque',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('cae547ca-02f2-4cdc-9b8d-f292d83b550c'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='loan',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('6585e97c-c842-419f-a4e6-39dfe2766aa3'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='loanfee',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('6ac8d712-0be3-44ca-bb1d-2fc5418fc59e'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='nhif',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('8c422413-ed4a-44b6-9c16-aa62a9e375e0'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='passbook',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('306cb96d-0a44-4b85-92ae-5e609456c73e'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='payments',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('970fcb9d-1072-4af1-b327-ac32f806436a'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='registration',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('42d6b666-0f73-4b4a-8a08-5cc83d2f0eb4'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='shares',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('eee2153b-047f-4e51-a840-c408ece99029'), max_length=200, unique=True),
        ),
    ]