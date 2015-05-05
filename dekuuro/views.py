from django.shortcuts import render
from dekuuro.forms import *
from dekuuro.models import *
from django.http import HttpResponseRedirect

# Create your views here.

def testView(Request):
	if Request.method == 'POST':
		formset = BoardForm(Request.POST)
		if formset.is_valid():
			return HttpResponseRedirect('')
	else:
		formset = BoardForm()
	return render(Request, 'test.html', { 'formset' : formset })

#TODO templates
def mainPageView(Request):
	return render(Request, 'main.html')
	
def registrationView(Request):
	return render(Request, 'register.html')
	
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
	
def createBoardView(Request):
	return render(Request, 'createBoard.html')
	
def boardTagsView(Request):
	return render(Request, 'boardTags.html')
	
def searchView(Request):
	return render(Request, 'searchView.html')
	
def inviteUsersView(Request):
	return render(Request, 'inviteUsers.html')
	
def userProfileView(Request):
	return render(Request, 'userProfile.html')
