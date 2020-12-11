from django import forms
from django.contrib.auth.forms import UserCreationForm
from employee.models import Employee
from django.contrib.auth import authenticate


class AccountAuthenticationForm(forms.ModelForm):
    pin = forms.CharField(label='pin', widget=forms.TextInput)


    class Meta:
        model = Employee
        fields = ('pin',)
    
    def clean(self):
        if self.is_valid():
            pin = self.cleaned_data['pin']
            