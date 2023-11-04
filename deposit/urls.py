from django.urls import path
from savings import views
from sacco.utils import HashIdConverter
from django.urls import path, register_converter
register_converter(HashIdConverter, "hashid")

app_name = "deposit"

urlpatterns = [
    path("withdrawal/", views.withdrawal, name="withdrawal-list"),
    path("withdrawal/add/", views.add_withdrawal, name="withdrawal-add"),
    path("<hashid:id>/edit/", views.edit_withdrawal, name="withdrawal-edit"),
    path("<hashid:withdrawal_id>/reciept/", views.withdrawl_reciept, name="withdrawal-reciept"),  
    path("<hashid:member_id>/statement/", views.statement, name="account-statement"), 

]