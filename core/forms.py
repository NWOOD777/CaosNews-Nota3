from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from captcha.fields import CaptchaField


class PeriodistaForm(ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Periodista
        fields = '__all__'  

class NoticiasForm(ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Noticia
        fields = '__all__'

class UserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']