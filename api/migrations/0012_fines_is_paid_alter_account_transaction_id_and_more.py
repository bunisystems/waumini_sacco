# Generated by Django 4.1.4 on 2023-04-23 09:35

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_fines_fine_no_fines_transaction_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='fines',
            name='is_paid',
            field=models.BooleanField(default=0),
        ),
        migrations.AlterField(
            model_name='account',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('d0c4c2cd-78ae-4bc4-88a9-803ef367607b'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='capitalshares',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('5e769591-42d7-453f-aef4-1e2dbbe5606a'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='cheque',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('7f4eee55-71c8-40f5-9d94-3507e764f042'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='fines',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('9c640180-86de-49d9-ad2b-6b302695c369'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='loan',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('e1051482-243b-4333-856d-823e98e1b221'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='loanfee',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('7abda444-874a-43c4-8851-aaa502ac33cb'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='nhif',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('bf5146b8-f1a2-47e1-97bc-65582854097f'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='passbook',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('7741e526-174e-4afc-b8e4-ff5cf3452cd8'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='payments',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('c9c00768-46f9-4ffe-8e47-e5e225fa8504'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='registration',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('c82cd474-72df-442b-8fa6-2f8e085ee6f8'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='shares',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('875ebe31-37aa-4e06-b7db-ab22b039ffc9'), max_length=200, unique=True),
        ),
    ]