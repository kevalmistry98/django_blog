from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from . models import profile
from django.core.exceptions import ValidationError

class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()
	class Meta:
		model = User
		fields = ['username', 'email', 'password1','password2']

	def clean_email(self):
		email = self.cleaned_data.get('email')
		em = User.objects.filter(email = email)
		if em.exists():
			raise forms.ValidationError("Email already taken, user other email id!")
		else:
			return email

class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = profile
		fields = ['image']