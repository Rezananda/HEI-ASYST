from django import forms
from django.contrib.auth.forms import UserCreationForm
from account.models import UserProfile
from django.contrib.auth.models import User

class UserModelForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password, minimal 8 Digit",}), label=False)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Konfirmasi Password",}), label=False)
    username= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Inisial, contoh : PMR', 'maxlength' : '3'}), label=False)    
    class Meta:
        model = User

        fields = ('username', 'password1', 'password2')
        # labels = {'username' : 'Inisial', 'password1' : 'Password', 'password2' : 'Konfirmasi Password'}
        help_texts = {
            'username': None
        }

class UserProfileModelForm(forms.ModelForm):
    full_name= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Nama Lengkap'}), label=False)
    class Meta:
        model = UserProfile
        fields = ['full_name']