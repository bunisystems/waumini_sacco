import django_tables2 as tables
from api.models import Registration

class PersonTable(tables.Table):
    class Meta:
        model = Registration
        template_name = "django_tables2/bootstrap.html"
        fields = ("name", )