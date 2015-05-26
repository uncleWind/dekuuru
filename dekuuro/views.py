from django.shortcuts import render
from dekuuro.forms import *
from dekuuro.models import *
from django.http import HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required

# Create your views here.

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

def logoutView(Request):
	logout(Request)
	return HttpResponseRedirect('/')

@login_required(login_url='login')
def createBoardView(Request):
	if Request.method == 'POST':
		formset = BoardForm(Request.POST)
		if formset.is_valid():
			newBoard = formset.save()
			boardUsr = BoardUsers(board=newBoard, user=Request.user, priviledge_level='ADM')
			boardUsr.save()
			return HttpResponseRedirect('/board/%s/' % (newBoard.board_tag))
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

def boardView(Request, boardTag):
	currBoard = Board.objects.get(board_tag=boardTag)
	images = Image.objects.filter(board=currBoard)
	tags = Tag.objects.filter(board=currBoard)
	return render(Request, 'board.html', {'images' : images , 'board' : currBoard, 'tags' : tags})

@login_required(login_url='login')
def addImageView(Request, boardTag):
	boardId = Board.objects.get(board_tag=boardTag)
	if Request.method == 'POST':
		formset = ImageForm(Request.POST, Request.FILES, boardId=boardId)
		if formset.is_valid():
			newImg = formset.save(commit=False)
			newImg.board = boardId
			newImg.uploader = Request.user
			newImg.save()
			formset.save_m2m()
			return HttpResponseRedirect('/board/%s/' % (boardTag))
	else:
		formset = ImageForm(boardId=boardId)
	return render(Request, 'addImage.html', { 'formset' : formset.as_p() , 'boardTag' : boardTag})

def boardsView(Request):
	boards = Board.objects.all()
	return render(Request, 'boards.html', { 'boards' : boards })

def imageDetailsView(Request, boardTag, boardImageID):
	board = Board.objects.get(board_tag=boardTag)
	image = Image.objects.get(board=board, boardID=boardImageID)
	if Request.method == 'POST' and Request.user.is_authenticated():
		formset = CommentForm(Request.POST)
		if formset.is_valid():
			comment = formset.save(commit=False)
			comment.poster = Request.user
			comment.image = image
			comment.save()
			formset = CommentForm()
	else:
		formset = CommentForm()
	comments = Comment.objects.filter(image=image)
	tags = image.tags.all()
	return render(Request, 'imageDetails.html', { 'formset':formset.as_p(), 'image':image, 'board':board, 'comments':comments, 'tags':tags})

def boardTagsView(Request, boardTag):
	board = Board.objects.get(board_tag=boardTag)
	if Request.method == 'POST' and Request.user.is_authenticated():
		formset = TagForm(Request.POST)
		if formset.is_valid():
			tag = formset.save(commit=False)
			tag.board = board
			tag.save()
			return HttpResponseRedirect('/board/%s/' % (boardTag))
	else:
		formset = TagForm()
	activeTags = Tag.objects.filter(board=board)
	return render(Request, 'boardTags.html', { 'formset':formset.as_p(), 'board':board, 'tags':activeTags })

def editTagView(Request, boardTag, tagName):
	board = Board.objects.get(board_tag=boardTag)
	if Request.method == 'POST' and Request.user.is_authenticated():
		formset = TagForm(Request.POST)
		if formset.is_valid():
			form_tag = formset.save(commit=False)
			tag = Tag.objects.get(board=board, name=tagName)
			if tag.name != form_tag.name:
				tag.name = form_tag.name
				tag.save()
				return HttpResponseRedirect('/board/%s/' % (boardTag))
			else:
				formset = TagForm(initial={'name':tagName})
	else:
		formset = TagForm(initial={'name':tagName})
	return render(Request, 'editTag.html', { 'formset':formset.as_p(), 'board':board, 'tag':tagName })

def removeTagView(Request, boardTag, tagName):
	board = Board.objects.get(board_tag=boardTag)
	tag = Tag.objects.get(board=board, name=tagName)
	tag.delete()
	return HttpResponseRedirect('/board/%s/' % (boardTag))

#TODO templates
def mainPageView(Request):
	return render(Request, 'main.html')

def profilesView(Request):
	return render(Request, 'profiles.html')

def profileView(Request):
	return render(Request, 'profile.html')

def subscriptionsView(Request):
	return render(Request, 'subscriptions.html')

def searchView(Request):
	return render(Request, 'search.html')

def inviteUsersView(Request):
	return render(Request, 'inviteUsers.html')

def userProfileView(Request):
	return render(Request, 'userProfile.html')
