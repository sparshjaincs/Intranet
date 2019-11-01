from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile

class SignUpForm(UserCreationForm):

    email = forms.EmailField(required=True,
                         label='Email',
                         error_messages={'exists': 'Oops'},
                         widget=forms.TextInput(attrs={'readonly':'readonly'}))
    username = forms.Field(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    first_name = forms.Field(widget=forms.TextInput(attrs={'readonly':'readonly'}))

    readonly_fields = ('username', 'first_name', 'email')
    class Meta:
        model = User
        fields = ("username", "first_name", "email", "password1", "password2")




class ProfileForm(forms.ModelForm):
    emp_type = forms.Field(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    pay_type = forms.Field(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    class Meta:
        model = Profile
        fields = ['pay_type', 'emp_type', 'contact', 'whatsapp', 'gender', 'avatar']
