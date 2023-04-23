from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from sacco.utils import HashIdConverter

from django.urls import URLResolver, path, register_converter
register_converter(HashIdConverter, "hashid")

urlpatterns = [
    path('sign-in', views.sign_in, name="sign-in"),
    path('sign-out/', views.sign_out, name="sign-out"),
    path('', views.index, name="index"),

    # Registration
    path('registration', views.registration, name="registration"),
    path('add-registration', views.add_registration, name="add-registration"),
    path('edit-registration/<hashid:id>', views.edit_registration, name="edit-registration"),


    # Loan
    path('loan', views.loan, name="loan"),
    path('payments', views.payments, name="payments"),
    path('paid-loan', views.paid_loan, name="paid-loan"),
    path('unpaid-loan', views.unpaid_loan, name="unpaid-loan"),
    path('loan-info/<hashid:id>', views.loan_info, name="loan-info"),
    path('loan-payments/<hashid:id>', views.loan_payments, name="loan-payments"),
    path('edit-loan-payments/<hashid:id>', views.edit_loan_payments, name="edit-loan-payments"),
    path('add-loan', views.add_loan, name="add-loan"),
    path('edit-loan/<hashid:id>', views.edit_loan, name="edit-loan"),

    # Fines
    path('fines', views.fine, name="fines"),
    path('add-fine/<hashid:id>', views.add_fine, name="add-fine"),

    path('loan-fee', views.loan_fee, name="loan-fee"),
    path('add-loan-fee', views.add_loan_fee, name="add-loan-fee"),
    path('edit-loan-fee/<hashid:id>', views.edit_loan_fee, name="edit-loan-fee"),



    # Capital Shares
    path('capital-shares', views.capital_shares, name="capital-shares"),
    path('add-capital-shares', views.add_capital_shares, name="add-capital-shares"),
    path('edit-capital-shares/<hashid:id>', views.edit_capital_shares, name="edit-capital-shares"),


    # Shares
    path('shares', views.shares, name="shares"),
    path('add-shares', views.add_shares, name="add-shares"),
    path('edit-shares/<hashid:id>', views.edit_shares, name="edit-shares"),


    # NHIF
    path('nhif', views.nhif, name="nhif"),
    path('add-nhif', views.add_nhif, name="add-nhif"),
    path('edit-nhif/<hashid:id>', views.edit_nhif, name="edit-nhif"),


    # Cheque
    path('cheque', views.cheque, name="cheque"),
    path('add-cheque', views.add_cheque, name="add-cheque"),
    path('edit-cheque/<hashid:id>', views.edit_cheque, name="edit-cheque"),


    # Account
    path('account', views.account, name="account"),
    path('add-account', views.add_account, name="add-account"),
    path('edit-account/<hashid:id>', views.edit_account, name="edit-account"),


     # Passbook
    path('passbook', views.passbook, name="passbook"),
    path('add-passbook', views.add_passbook, name="add-passbook"),
    path('edit-passbook/<hashid:id>', views.edit_passbook, name="edit-passbook"),



    
    path('settings', views.settings, name="settings"),

    # Reciepts
    path('r1/<hashid:id>', views.registration_reciept, name="r1"),
    path('r2/<hashid:id>', views.capitalshare_reciept, name="r2"),
    path('r3/<hashid:id>', views.nhif_reciept, name="r3"),
    path('r4/<hashid:id>', views.account_reciept, name="r4"),
    path('r5/<hashid:id>', views.shares_reciept, name="r5"),
    path('r6/<hashid:id>', views.loanfee_reciept, name="r6"),
    path('r7/<hashid:id>', views.cheque_reciept, name="r7"),
    path('r8/<hashid:id>', views.passbook_reciept, name="r8"),
    path('r9/<hashid:id>', views.payments_reciept, name="r9"),

    # # User
    path('users', views.users, name="users"),
    path('add-user', views.add_user, name="add-user"),
    path('edit-user/<hashid:id>', views.edit_user, name="edit-user"),
    path('delete-user/<hashid:id>', views.delete_user, name="delete-user"),

    path('members', views.members, name="members"),
    path('add-member', views.add_member, name="add-member"),
    path('edit-member/<hashid:id>', views.edit_member, name="edit-member"),
    path('delete-user/<hashid:id>', views.delete_user, name="delete-user"),


    path('profile/<hashid:id>', views.profile, name="profile"),
   


    # Password Reset
    path('reset_password/', 
	auth_views.PasswordResetView.as_view(template_name='sacco/auth/password_reset.html'), 
	name="reset_password"),

	path('reset_password_sent/', 
	auth_views.PasswordResetDoneView.as_view(template_name='sacco/auth/password_reset_sent.html'), 
	name="password_reset_done"),

	path('reset/<uidb64>/<token>/', 
	auth_views.PasswordResetConfirmView.as_view(template_name='sacco/auth/password_reset_form.html'), 
	name="password_reset_confirm"),

	path('reset_password_complete/', 
	auth_views.PasswordResetCompleteView.as_view(template_name='sacco/auth/password_reset_done.html'), 
	name="password_reset_complete"),
]