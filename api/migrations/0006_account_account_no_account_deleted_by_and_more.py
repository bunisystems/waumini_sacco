# Generated by Django 4.1.4 on 2023-01-18 12:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0005_capitalshares_c_share_no_capitalshares_deleted_by_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='account_no',
            field=models.CharField(default=django.utils.timezone.now, max_length=200, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='account',
            name='deleted_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='account_deleted_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='account',
            name='deleted_on',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='is_deleted',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='account',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('e4136765-deab-494f-a512-a7ac1a111909'), max_length=200, unique=True),
        ),
        migrations.AddField(
            model_name='account',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='account_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='account',
            name='updated_on',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='cheque',
            name='cheque_no',
            field=models.CharField(default=django.utils.timezone.now, max_length=200, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cheque',
            name='deleted_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cheque_deleted_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cheque',
            name='deleted_on',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='cheque',
            name='is_deleted',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='cheque',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('5f58a8c5-76a8-420b-897e-aa405046b0ff'), max_length=200, unique=True),
        ),
        migrations.AddField(
            model_name='cheque',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cheque_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cheque',
            name='updated_on',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='nhif',
            name='deleted_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nhif_deleted_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='nhif',
            name='deleted_on',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='nhif',
            name='is_deleted',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='nhif',
            name='nhif_no',
            field=models.CharField(default=django.utils.timezone.now, max_length=200, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='nhif',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('967ebe64-3a48-42ed-bf47-cd9a62011f72'), max_length=200, unique=True),
        ),
        migrations.AddField(
            model_name='nhif',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nhif_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='nhif',
            name='updated_on',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='passbook',
            name='deleted_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='passbook_deleted_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='passbook',
            name='deleted_on',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='passbook',
            name='is_deleted',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='passbook',
            name='passbook_no',
            field=models.CharField(default=django.utils.timezone.now, max_length=200, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='passbook',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('6349d68c-a14a-41fb-a7b1-4850ebc25222'), max_length=200, unique=True),
        ),
        migrations.AddField(
            model_name='passbook',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='passbook_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='passbook',
            name='updated_on',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='processing',
            name='deleted_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='processing_deleted_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='processing',
            name='deleted_on',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='processing',
            name='is_deleted',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='processing',
            name='processing_no',
            field=models.CharField(default=django.utils.timezone.now, max_length=200, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='processing',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('5a0c11b5-6e2c-4fa3-9302-93a203c8c876'), max_length=200, unique=True),
        ),
        migrations.AddField(
            model_name='processing',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='processing_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='processing',
            name='updated_on',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='capitalshares',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('e143e457-9d1c-44b4-a1a9-d633185a6d2a'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='loan',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('38bb1170-c0ca-4d08-980b-dce51c105ff0'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='payments',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('4c91eb38-8d91-4fd3-b908-834a7146ca7c'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='registration',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('4793f749-25ba-4561-a3aa-b6b2b6643329'), max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='shares',
            name='transaction_id',
            field=models.CharField(default=uuid.UUID('df01de4d-e99c-4f61-be52-6beb5a96040d'), max_length=200, unique=True),
        ),
    ]
