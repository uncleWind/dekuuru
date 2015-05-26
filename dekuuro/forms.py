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
		fields = ('name',)

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
	password2 = forms.CharField(label='Confirm password')

	class Meta:
		model = User
		fields = ('username', 'password', 'password2', 'email')
		widgets = {
			'password'	: forms.PasswordInput(),
			'password2'	: forms.PasswordInput(),
		}

class LoginForm(forms.Form):
	username = forms.CharField(label='Username', max_length=30)
	password = forms.CharField(label='Password', widget=forms.PasswordInput())

class BoardForm(ModelForm):
	class Meta:
		model = Board
		fields = '__all__'
