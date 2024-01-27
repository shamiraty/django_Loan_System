from django import forms
from .models import  Loan
# class
class CustomerLoan(forms.ModelForm):
    class Meta:
        model = Loan
        fields = "__all__"
