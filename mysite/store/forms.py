from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm
from .models import ShoppingCartDetail

User = get_user_model()

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        if commit:
            user.save()
        return user


class CashPaymentForm(forms.Form):
    cash_amount = forms.DecimalField(max_digits=6, decimal_places=2)


class CardPaymentForm(forms.Form):
    card_amount = forms.DecimalField(max_digits=6, decimal_places=2)
