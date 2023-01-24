from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('sign-in', views.sign_in, name="sign-in"),
    path('sign-out/', views.sign_out, name="sign-out"),
    path('', views.index, name="index"),

    # Registration
    path('registration', views.registration, name="registration"),
    path('add-registration', views.add_registration, name="add-registration"),
    path('edit-registration/<int:id>', views.edit_registration, name="edit-registration"),


    # Loan
    path('loan', views.loan, name="loan"),
    path('paid-loan', views.paid_loan, name="paid-loan"),
    path('unpaid-loan', views.unpaid_loan, name="unpaid-loan"),
    path('loan-info/<int:id>', views.loan_info, name="loan-info"),
    path('loan-payments/<int:id>', views.loan_payments, name="loan-payments"),
    path('add-loan', views.add_loan, name="add-loan"),
    path('edit-loan/<int:id>', views.edit_loan, name="edit-loan"),



    # Capital Shares
    path('capital-shares', views.capital_shares, name="capital-shares"),
    path('add-capital-shares', views.add_capital_shares, name="add-capital-shares"),
    path('edit-capital-shares/<int:id>', views.edit_capital_shares, name="edit-capital-shares"),


    # Shares
    path('shares', views.shares, name="shares"),
    path('add-shares', views.add_shares, name="add-shares"),
    path('edit-shares/<int:id>', views.edit_shares, name="edit-shares"),


    # NHIF
    path('nhif', views.nhif, name="nhif"),
    path('add-nhif', views.add_nhif, name="add-nhif"),
    path('edit-nhif/<int:id>', views.edit_nhif, name="edit-nhif"),


    # Cheque
    path('cheque', views.cheque, name="cheque"),
    path('add-cheque', views.add_cheque, name="add-cheque"),
    path('edit-cheque/<int:id>', views.edit_cheque, name="edit-cheque"),


    # Account
    path('account', views.account, name="account"),
    path('add-account', views.add_account, name="add-account"),
    path('edit-account/<int:id>', views.edit_account, name="edit-account"),


    # Processing
    path('processing', views.processing, name="processing"),
    path('add-processing', views.add_processing, name="add-processing"),
    path('edit-processing/<int:id>', views.edit_processing, name="edit-processing"),


     # Passbook
    path('passbook', views.passbook, name="passbook"),
    path('add-passbook', views.add_passbook, name="add-passbook"),
    path('edit-passbook/<int:id>', views.edit_passbook, name="edit-passbook"),


    path('settings', views.settings, name="settings"),




    # Entrance

    # path('add-station', views.add_station, name="add-station"),
    # path('edit-station/<int:id>', views.edit_station, name="edit-station"),
    # path('delete-station/<int:id>', views.delete_station, name="delete-station"),

    # # Float
    # path('float', views.float, name="float"),
    # path('add-float', views.add_float, name="add-float"),
    # path('edit-float/<int:id>', views.edit_float, name="edit-float"),
    # path('delete-float/<int:id>', views.delete_float, name="delete-float"),

    # # Expense
    # path('expense', views.expense, name="expense"),
    # path('my-expense', views.my_expense, name="my-expense"),
    # path('add-expense', views.add_expense, name="add-expense"),
    # path('edit-expense/<int:id>', views.edit_expense, name="edit-expense"),
    # path('delete-expense/<int:id>', views.delete_expense, name="delete-expense"),

    # # User
    path('users', views.users, name="users"),
    path('add-user', views.add_user, name="add-user"),
    path('edit-user/<int:id>', views.edit_user, name="edit-user"),
    path('delete-user/<int:id>', views.delete_user, name="delete-user"),

    path('members', views.members, name="members"),
    path('add-member', views.add_user, name="add-member"),
    path('edit-member/<int:id>', views.edit_user, name="edit-member"),
    path('delete-user/<int:id>', views.delete_user, name="delete-user"),


    path('profile/<int:id>', views.profile, name="profile"),
    path('member/<int:id>', views.member, name="member"),

    # # Reports
    # path('float-vs-expense', views.float_vs_expense, name="float-vs-expense"),
    # path('user-expense', views.user_expense, name="user-expense"),
    # path('all-user-expense', views.all_user_expense, name="all-user-expense"),
    # path('user-expense-advanced-reports', views.user_expense_advanced_reports, name="user-expense-advanced-reports"),
    # path('float-vs-expense-advanced-reports', views.float_vs_expense_advanced_reports, name="float-vs-expense-advanced-reports"),


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