from django.forms import ModelForm, widgets
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import *
from api.models import Settings

class CreateUserForm(UserCreationForm):
	group = forms.CharField()
	class Meta:
		model = User
		fields = UserCreationForm.Meta.fields + ('username', 'email', 'first_name', 'last_name', 'group')
	
class  SettingsForm(forms.ModelForm):
	class Meta:
		model = Settings
		fields = [
			'REGISTRATION_FEE',
			'MIN_LOAN',
			'MAX_LOAN',
			'CAPITAL_SHARE',
			'SHARES_MIN',
			'ACCOUNT',
			'ACCOUNT_WITHDRAWAL',
			'PROCESSING_FEE',
			'PASSBOOK',
			'INTEREST',
			'INSUARANCE',
			'PHONE_NUMBER'
		]


