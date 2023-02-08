from django.forms import ModelForm, widgets
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from api.models import *
from api.models import Settings

class CreateUserForm(UserCreationForm):
	group = forms.CharField()
	email = forms.EmailField(required=False)
	password1 = forms.CharField(required=False)
	password2 = forms.CharField(required=False)
	class Meta:
		model = User
		fields = UserCreationForm.Meta.fields + ('username', 'email', 'first_name', 'last_name', 'group', 'is_active')
		required_fields = ('group', 'first_name', 'last_name', 'username', 'is_active')

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('member_no_shares', 'member_no_savings', 'id_no')
		required_fields = ('id_no',)
	
class  SettingsForm(forms.ModelForm):
	class Meta:
		model = Settings
		fields = [
			'SHARES_ENTRANCE_FEE',
			'SHARES_APPLICATION_FEE',
			'SAVINGS_ENTRANCE_FEE',
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


