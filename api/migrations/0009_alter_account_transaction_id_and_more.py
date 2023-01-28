# Generated by Django 4.1.4 on 2023-01-23 07:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
        ('api', '0008_alter_account_transaction_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('9b8bf93b-d1c1-427f-b102-25c6d1d7def6'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='capitalshares',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('48606b2e-e68d-49e5-ac37-303088b9a2cf'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='cheque',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('c27d5dd3-7a3c-4eb4-ae43-c220d6827bf9'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='loan',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('7030b39b-78b5-4c66-8a4b-a0105df50de7'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='nhif',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('26d3bca7-3f72-4392-89b0-48c880e1f3a0'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='passbook',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('4d67c97f-65bb-4140-b049-251bf8e80675'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='payments',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('9c912701-fd77-48df-9b88-818e6b066352'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='processing',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('81fd1afa-edcd-4bf8-b18f-17b375489bdf'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='registration',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('0af583df-9639-4d19-ab52-fc854afd3615'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='shares',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('4834e2e2-784f-4d28-8919-81e16f0e0bfe'), max_length=200, unique=True),
        ),
        migrations.CreateModel(
            name='settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('REGISTRATION_FEE', models.IntegerField()),
                ('MIN_LOAN', models.IntegerField()),
                ('MAX_LOAN', models.IntegerField()),
                ('CAPITAL_SHARE', models.IntegerField()),
                ('SHARES_MIN', models.IntegerField()),
                ('ACCOUNT', models.IntegerField()),
                ('ACCOUNT_WITHDRAWAL', models.IntegerField()),
                ('PROCESSING_FEE', models.IntegerField()),
                ('PASSBOOK', models.IntegerField()),
                ('INTEREST', models.IntegerField()),
                ('INSUARANCE', models.IntegerField()),
                ('PHONE_NUMBER', models.IntegerField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(null=True)),
                ('deleted_on', models.DateTimeField(null=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='settings_deleted_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='settings_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]