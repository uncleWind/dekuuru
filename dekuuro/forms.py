from django import forms
from django.forms import ModelForm
from dekuuro.models import *
from django.contrib.auth.models import User

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
		fields = ('name', 'password', 'mail')
		widgets = {
			'password' : forms.PasswordInput(),
		}

class LoginForm(ModelForm)
	class Meta:
		model = User
		fields = ('name', 'password')
		widgets = {
			'password' : forms.PasswordInput(),
		}

class BoardForm(ModelForm):
	class Meta:
		model = Board
		fields = '__all__'
