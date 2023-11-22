# class UserProfile(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     address = models.CharField(max_length=255, blank=True, null=True)
#     city = models.CharField(max_length=255, blank=True, null=True)
#     state = models.CharField(max_length=2, blank=True, null=True)
#     zip_code = models.CharField(max_length=5, blank=True, null=True)
#     phone = PhoneNumberField(blank=True, null=True)
#     date_of_birth = models.DateField(blank=True, null=True)
#     gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
#     profile_picture = models.ImageField(upload_to='profile_pics', blank=True, null=True)
#     bio = models.TextField(blank=True, null=True)
#     additional_info = models.TextField(blank=True, null=True)


#     def __str__(self):
#         return f"{self.user.username}'s profile"


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile
from django.forms import ModelForm


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.save()
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        user_profile.save()
        if commit:
            return user







# class CartForm(forms.Form):
#     quantity = forms.IntegerField(min_value=1)
#     price = forms.DecimalField(min_value=10.00)


# class WorkOrderForm(forms.Form):
#     service_description = forms.CharField(label='Description', max_length=255)
#     service_cost = forms.DecimalField(label='Price', min_value=10.00)
