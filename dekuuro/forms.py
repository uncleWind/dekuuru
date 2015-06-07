from django import forms
from django.forms import ModelForm
from dekuuro.models import *
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

class CommentForm(ModelForm):
	class Meta:
		model = Comment
		fields = ('content',)

class TagForm(ModelForm):
	class Meta:
		model = Tag
		fields = ('name',)

class MissingTagsForm(ModelForm):
	def __init__(self, *args, **kwargs):
		image = kwargs.pop('image')

		super(MissingTagsForm, self).__init__(*args, **kwargs)
		self.fields['tags'] = forms.ModelMultipleChoiceField(required=True, queryset=Tag.objects.filter(board=image.board).exclude(name__in = image.tags.values_list('name', flat=True)))

	class Meta:
		model = Image
		fields = ('tags',)

class ImageForm(ModelForm):
	def __init__(self, *args, **kwargs):
		boardId = kwargs.pop('boardId')
		super(ImageForm, self).__init__(*args, **kwargs)
		self.fields['tags'] = forms.ModelMultipleChoiceField(
                required=True,
                queryset=Tag.objects.filter(board=boardId))

	class Meta:
		model = Image
		fields = ('URI', 'tags')


class UserForm(ModelForm):
	password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'password', 'password2', 'email')
		widgets = {
			'password'	: forms.PasswordInput(),
		}
	
	def clean_email(self):
		mail = self.cleaned_data['email']
		if User.objects.filter(email=mail).exists():
			raise ValidationError('Email already exists')
		return mail
	
	def clean(self):
		data = self.cleaned_data
		if data['password'] != data['password2']:
			self._errors['password'] = ['Passwords do not match']
			del data['password']
			del data['password2']
		return data

class LoginForm(forms.Form):
	username = forms.CharField(label='Username', max_length=30)
	password = forms.CharField(label='Password', widget=forms.PasswordInput())

class BoardForm(ModelForm):
	class Meta:
		model = Board
		fields = '__all__'

class SearchForm(forms.Form):
	searchString = forms.CharField(label='Search', max_length=1000)

class BoardUserForm(ModelForm):
	user = forms.CharField(max_length=30)
	
	class Meta:
		model = BoardUsers
		fields = ('user','priviledge_level')
	
	def clean(self):
		data = self.cleaned_data
		if not User.objects.filter(username=data['user']).exists():
			self._errors['user'] = ['User does not exist']
			del data['user']
		else:
			data['user'] = User.objects.get(username=data['user'])
		return data
	
	#def save(self, commit=False):
	#	username = self.cleaned_data['user']
	#	usr = User.objects.get(username=username)
	#	self.instance.user = usr
	#	
	#	return super(BoardUserForm, self).save(commit)
		
