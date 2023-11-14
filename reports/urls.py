from django.urls import path
from reports import views
from sacco.utils import HashIdConverter
from django.urls import path, register_converter
register_converter(HashIdConverter, "hashid")

app_name = "reports"

urlpatterns = [
    path("members/", views.members, name="members"),
    path("registration/", views.registration, name="registration"),
    path("capital_shares/", views.capital_shares, name="capital_shares"),
    path("nhif/", views.nhif, name="nhif"),
    path("shares_account/", views.shares, name="shares_account"),
    path("deposits/", views.account, name="account"),
    path("withdrawal/", views.withdrawal, name="withdrawal"),
    path("cheque/", views.cheque, name="cheque"),
    path("passbook/", views.passbook, name="passbook"),
]