from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    roles = forms.ChoiceField(choices=CustomUser.ROLES_CHOICES, widget=forms.RadioSelect)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = fields = ["username", "password1", "password2", "roles"]

class CustomUserEditForm(UserChangeForm):
    password = None 
    roles = forms.ChoiceField(choices=CustomUser.ROLES_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = CustomUser
        fields = ["username", "roles"]

    def clean_password(self):
        return self.initial["password"]