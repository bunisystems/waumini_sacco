# Generated by Django 4.1.4 on 2023-02-17 16:16

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_alter_account_transaction_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('16f4b12b-e013-4fa9-9a14-3a3f42a7c91c'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='capitalshares',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('a858ac17-ad72-4a48-bdaf-be8ee599888d'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='cheque',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('2e684608-31e8-44b4-81aa-157c24059f82'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='loan',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('714c66a1-0336-4abf-9fe2-0e9ae1d62c08'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='loanfee',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('1a3e119b-8144-4744-9ab8-46a16e33677b'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='nhif',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('0c05e85c-3804-4c04-bd6a-4d22ad7a7b8a'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='passbook',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('6e23cbb5-9095-4600-9dc4-ff292c520501'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='payments',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('4cc21bde-1d06-4155-81a4-c209200adcd9'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='registration',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('b8e64a1d-23d2-4f57-a315-7ba83c6c08db'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='shares',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('d18ce30d-0b81-46a4-89f4-6378ebb6ba71'), max_length=200, unique=True),
        ),
    ]