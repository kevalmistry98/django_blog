from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

# user verification imports
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from . utils import token_generator
#===============================================================

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			user = form.save(commit = False)
			user.is_active = False
			user.save()
			username = form.cleaned_data.get('username')
			email_add = form.cleaned_data.get('email')
			uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
			domain = get_current_site(request).domain
			link = reverse('activate', kwargs = {'uidb64':uidb64, 'token': token_generator.make_token(user)})
			activate_url = 'http://'+ domain + link
			email_subject = 'Activate your account'
			email_body = f'Hi {username}, please click on the below mentioned link and activate your account so that you can log into your AmatuerScribbbles.com\n ' + activate_url
			email_msg = EmailMessage(
				email_subject,
				email_body,
				'no-reply',
				[email_add]
			)
			email_msg.send(fail_silently = False)
			messages.success(request, f'An activation email has been sent to your registered email address, please activate your account to login into your account!')
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request , 'users/register.html', {'form': form})



def verification(View, *args ,**kwargs):
	def get(self, request, uidb64, token):
		return redirect('login')


@login_required
def profile(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance = request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance = request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f'your account has been successfully updated')
			return redirect('profile')
	else:
		u_form = UserUpdateForm(instance = request.user)
		p_form = ProfileUpdateForm(instance = request.user.profile)
	
	context = {
		'u_form': u_form,
		'p_form': p_form

	}

	return render(request, 'users/profile.html', context)