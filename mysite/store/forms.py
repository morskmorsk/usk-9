from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

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






# class CartForm(forms.Form):
#     quantity = forms.IntegerField(min_value=1)
#     price = forms.DecimalField(min_value=10.00)


# class WorkOrderForm(forms.Form):
#     service_description = forms.CharField(label='Description', max_length=255)
#     service_cost = forms.DecimalField(label='Price', min_value=10.00)
