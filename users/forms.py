from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'username'})
        self.fields['email'].widget.attrs.update({'placeholder':'email'})
        self.fields['password1'].widget.attrs.update({'placeholder':'password'})
        self.fields['password2'].widget.attrs.update({'placeholder':'confirm password'})



class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    email.widget.attrs.update({'class': 'user-email'})

    class Meta:
        model = User
        fields = ['email',]



class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'image',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bio'].widget.attrs.update({'class': 'user-bio'})
        self.fields['location'].widget.attrs.update({'class':'user-location'})
        self.fields['image'].widget.attrs.update({'class':'user-image'})

class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'placeholder': 'username', 'id':'id_username_login'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'password'}))