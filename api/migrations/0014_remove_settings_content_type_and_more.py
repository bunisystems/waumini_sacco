# Generated by Django 4.1.4 on 2023-01-23 09:13

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_alter_account_transaction_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='settings',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='settings',
            name='object_id',
        ),
        migrations.AlterField(
            model_name='account',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('cca183d3-49ea-45f3-873e-e737db0ed06b'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='capitalshares',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('1b52669f-b0d2-4990-8c60-94ae03dff37e'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='cheque',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('0c9108ec-1b94-4ba4-afe2-360f31db2f0f'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='loan',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('8f158493-c086-464b-8424-c7191b52f09a'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='nhif',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('f63bb3c9-942c-47ec-9832-aef47ef21691'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='passbook',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('0cbce824-7f06-40e7-9bab-f872bf0481ec'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='payments',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('22bcad57-3513-43bf-bee9-9ef341f17997'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='processing',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('22fc4da7-c190-4c39-976b-74e3158cc534'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='registration',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('d70a788f-3fe8-4c91-9bdd-aa7bbce0dda3'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='shares',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('49cb6a40-3b17-4bba-904e-d95a9fccf7ad'), max_length=200, unique=True),
        ),
    ]