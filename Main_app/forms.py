from .models import *
from django import forms


class userform(forms.ModelForm):
    username = forms.CharField(required=True, label=('Username'))
    password = forms.CharField(required=False, label=('Password'))
    father_name = forms.CharField(required=False, label='Father name')
    mother_name = forms.CharField(required=False, label='Mother name')
    phone = forms.CharField(required=False, label='Phone')

    class Meta:
        model = Student
        fields = ['username', 'password', 'father_name', 'mother_name']

    widgets = {
        "username": forms.TextInput(attrs={'class': 'form-control'}),
        "password": forms.PasswordInput(attrs={'class': 'form-control'}),
        "father_name": forms.TextInput(attrs={'class': 'form-control'}),
        "mother_name": forms.TextInput(attrs={'class': 'form-control'}),
        "phone": forms.NumberInput(attrs={'class': 'form-control'}),

    }
