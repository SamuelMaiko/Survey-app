from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

class RegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=["username","email","password1", "password2"]
        
    # def clean_password2(self):
    #     password1=self.cleaned_data.get("password1")
    #     password2=self.cleaned_data.get("password2")
        
    #     if password1 and password2 and password1 != password2:
    #         raise forms.ValidationError("my custom comment")
        
    #     return password2
        
class LoginForm(AuthenticationForm):
    class Meta:
        model=User
        fields=["username","password"] 