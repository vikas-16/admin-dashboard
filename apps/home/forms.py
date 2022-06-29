from logging import PlaceHolder
from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import *


class Studentregistration(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name','email','password']
        
        widgets= {
            'name': forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}),
            'email': forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'}),
            'password': forms.PasswordInput(render_value=True, attrs={'class':'form-control', 'autocomplete':'off'}),
            }
