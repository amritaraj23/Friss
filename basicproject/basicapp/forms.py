from django import forms
from django.core import validators
from django.contrib.auth.models import User

def check_for_z(value):
    if value[0].lower() != 'z':
        raise forms.ValidationError("Name should start with Z")


class FormPerson(forms.Form):
    Person1_name = forms.CharField()
    Person1_birthday = forms.DateField(input_formats=["%d-%m-%Y"],required=False)
    Person1_bsn = forms.CharField(required=False)
    #botcatcher = forms.CharField(required=False, widget=forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])
    Person2_name = forms.CharField()
    Person2_birthday = forms.DateField(input_formats=["%d-%m-%Y"],required=False)
    Person2_bsn = forms.CharField(required=False)

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username','email','password')
    