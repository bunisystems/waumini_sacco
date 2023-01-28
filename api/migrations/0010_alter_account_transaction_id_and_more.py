# Generated by Django 4.1.4 on 2023-01-23 07:44

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
            field=models.CharField(default=uuid.UUID('361b8ad5-7635-4557-a54e-2179daaa9b0f'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='capitalshares',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('fd8bbc9e-8ea7-48ba-899a-295a5027bbbb'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='cheque',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('a8880bf3-4a82-4ee8-8aac-490cadae3a1b'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='loan',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('d751245d-3c00-49c1-8faa-5c41e41a2cf5'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='nhif',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('46522e8c-1c3c-465a-9bc5-7f283adf23c7'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='passbook',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('45a1d61b-84d0-49bf-b87e-eb640a95f3e8'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='payments',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('afffe5b8-52bf-4333-bf5e-cd0cd80ac197'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='processing',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('b789e3ae-8ce4-44bb-a5a6-cafb0fa145e9'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='registration',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('480ce591-c345-484d-8551-ab90febff6e2'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='shares',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('4f2b3acf-9d12-46ec-b62e-46560dcf10af'), max_length=200, unique=True),
        ),
    ]