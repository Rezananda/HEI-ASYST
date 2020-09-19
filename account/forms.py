from django import forms
from account.models import UserProfile
from django.contrib.auth.models import User

class UserModelForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password",}), label=False)
    username= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Inisial'}), label=False)
    class Meta:
        model = User
        fields = ['username', 'password']
        labels = {'username' : 'Inisial', 'password' : 'Password'}
        help_texts = {
            'username': None
        }

class UserProfileModelForm(forms.ModelForm):
    full_name= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Nama Lengkap'}), label=False)
    class Meta:
        model = UserProfile
        fields = ['full_name']
        labels = {'full_name' : 'Nama Lengkap'}