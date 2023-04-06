# Generated by Django 4.1.4 on 2023-03-16 13:12

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('ec604fb2-3c45-4881-a0b5-b80b2942e0db'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='capitalshares',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('2906910c-bec5-4058-a08d-702fea4359a7'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='cheque',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('0c6f1ffb-716c-4617-9b57-df01fcd2a9c7'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='loan',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('4921ca36-4265-41ab-b294-b80448bd2eef'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='loanfee',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('09da705b-f312-4a7a-8d56-ac1410718e84'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='nhif',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('2010ebca-6d8e-41be-a15a-f28f03ece660'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='passbook',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('1dc29f26-a575-4503-b50f-9c5d14c8fd0d'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='payments',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('68f9222e-072d-4a77-9cbb-ede642f8dcfc'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='registration',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('1bc9cb70-edbb-4ea9-a30c-2787f74ddba0'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='shares',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('7d354049-a79f-414a-a201-291be05fee28'), max_length=200, unique=True),
        ),
    ]