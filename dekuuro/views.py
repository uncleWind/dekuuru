from django.shortcuts import render
from dekuuro.forms import *
from dekuuro.models import *
from django.http import HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required

# Create your views here.

def testView(Request):
	if Request.method == 'POST':
		formset = BoardForm(Request.POST)
		if formset.is_valid():
			return HttpResponseRedirect('')
	else:
		formset = BoardForm()
	return render(Request, 'test.html', { 'formset' : formset })

def loginView(Request):
	logout(Request)
	loginError = ''
	if Request.method == 'POST':
		formset = LoginForm(Request.POST)
		if formset.is_valid():
			username = formset.cleaned_data['username']
			password = formset.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(Request, user)
					return HttpResponseRedirect('/')
			loginError = 'Login data incorrect.'
	else:
		formset = LoginForm()
	return render(Request, 'login.html', { 'formset' : formset.as_p(), 'loginError' : loginError})

@login_required(login_url='login')
def createBoardView(Request):
	if Request.method == 'POST':
		formset = BoardForm(Request.POST)
		if formset.is_valid():
			#TODO Validate, Give admin rights, set stuff
			return HttpResponseRedirect('')
	else:
		formset = BoardForm()
	return render(Request, 'createBoard.html', { 'formset' : formset.as_p() })
	
def registrationView(Request):
	if Request.method == 'POST':
		formset = UserForm(Request.POST)
		if formset.is_valid():
			#TODO Validate, Give admin rights, set stuff
			return HttpResponseRedirect('')
	else:
		formset = UserForm()
	return render(Request, 'register.html', { 'formset' : formset.as_p() })
	
#TODO templates
def mainPageView(Request):
	return render(Request, 'main.html')
	
def boardView(Request):
	return render(Request, 'board.html')

def addImageView(Request):
	return render(Request, 'addImage.html')

def profilesView(Request):
	return render(Request, 'profiles.html')
	
def profileView(Request):
	return render(Request, 'profile.html')
	
def imageDetailsView(Request):
	return render(Request, 'imageDetails.html')
	
def subscriptionsView(Request):
	return render(Request, 'subscriptions.html')
	
def boardTagsView(Request):
	return render(Request, 'boardTags.html')
	
def searchView(Request):
	return render(Request, 'search.html')
	
def inviteUsersView(Request):
	return render(Request, 'inviteUsers.html')
	
def userProfileView(Request):
	return render(Request, 'userProfile.html')
