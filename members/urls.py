from django.urls import path
from members import views
from sacco.utils import HashIdConverter
from django.urls import path, register_converter
register_converter(HashIdConverter, "hashid")

app_name = "members"

urlpatterns = [
    path('', views.members, name="member_list"),
    path('add', views.add_member, name="add-member"),
    path('<hashid:id>/edit/', views.edit_member, name="edit-member"),
    #path('<hashid:id>/delete', views.delete_user, name="delete-user"),

]