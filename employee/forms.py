from django import forms

from employee.models import Employee


class AccountAuthenticationForm(forms.ModelForm):

    pin = forms.CharField(
        label='pin',
        widget=forms.TextInput
    )

    class Meta:
        model = Employee
        fields = (
            'pin',
        )

    def clean(self):
        if self.is_valid():
            pin = self.cleaned_data[
                'pin'
            ]
