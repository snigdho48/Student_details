from .models import *
from django import forms


class userform(forms.ModelForm):
    username = forms.CharField(required=True, label=('Username'),widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(required=False, label=('Password'),widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    father_name = forms.CharField(required=False, label='Father name',widget=forms.TextInput(attrs={'class': 'form-control'}))
    mother_name = forms.CharField(required=False, label='Mother name',widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(required=False, label='Phone',widget= forms.NumberInput(attrs={'class': 'form-control'}))


    class Meta:
        model = Student
        fields = ['username', 'password', 'father_name', 'mother_name']