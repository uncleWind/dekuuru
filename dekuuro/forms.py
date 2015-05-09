from django import forms
from django.forms import ModelForm
from dekuuro.models import *
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class CommentForm(ModelForm):
	class Meta:
		model = Comment
		fields = ('content',)

class TagForm(ModelForm):
	class Meta:
		model = Tag
		fields = '__all__'

class ImageForm(ModelForm):
	class Meta:
		model = Image
		fields = ('URI', 'tags')

class UserForm(ModelForm):
	class Meta:
		model = User
		fields = ('username', 'password', 'email')
		widgets = {
			'password' : forms.PasswordInput(),
		}

class LoginForm(ModelForm):
	class Meta:
		model = User
		fields = ('username', 'password')
		widgets = {
			'password' : forms.PasswordInput(),
		}
		labels = {
			'password' : _('Password:')
		}
		help_texts = {
			'username' : _('')
		}

class BoardForm(ModelForm):
	class Meta:
		model = Board
		fields = '__all__'
