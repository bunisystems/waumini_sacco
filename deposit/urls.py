from django.urls import path
from deposit import views
from sacco.utils import HashIdConverter
from django.urls import path, register_converter
register_converter(HashIdConverter, "hashid")

app_name = "deposit"

urlpatterns = [
    path("", views.deposits, name="deposit-list"),
    path("add/", views.add_deposit, name="deposit-add"),
    path("<hashid:id>/edit/", views.edit_deposit, name="deposit-edit"),
    path("<hashid:deposit_id>/reciept/", views.deposit_receipt, name="deposit-reciept"),  
]