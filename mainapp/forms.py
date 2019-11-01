from django.forms import ModelForm
from .models import NewProvisionalEmployeeMail

class NewProvisionalEmployeeMailForm(ModelForm):
    class Meta:
        model = NewProvisionalEmployeeMail
        fields = ['email', 'position_name',
        'name', 'username', 'pay',
        'title', 'pay_type', 'emp_type',
        ]
