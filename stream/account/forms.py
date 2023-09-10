from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label='Username',widget=forms.TextInput,required=True)
    email = forms.EmailField(label='Email',widget=forms.TextInput, required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
