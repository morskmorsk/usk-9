from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

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


class AddToCartForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['quantity']

