from django.urls import path
from nhif import views
from sacco.utils import HashIdConverter
from django.urls import path, register_converter
register_converter(HashIdConverter, "hashid")

app_name = "nhif"

urlpatterns = [
    path("", views.nhif, name="nhif-list"),
    path("nhif/add/", views.add_nhif, name="nhif-add"),
    path("<hashid:id>/edit/", views.edit_nhif, name="nhif-edit"),
    path("<hashid:nhif_id>/reciept/", views.nhif_reciept, name="nhif-reciept"),  

]