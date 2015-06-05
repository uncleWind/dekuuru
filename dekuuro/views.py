from django.shortcuts import render
from dekuuro.forms import *
from dekuuro.models import *
from django.http import HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
	return render(Request, 'login.html', { 'formset' : formset.as_p(), 'loginError' : loginError, 'search_form' : SearchForm()})

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
	return render(Request, 'createBoard.html', { 'formset' : formset.as_p(), 'search_form' : SearchForm() })

def registrationView(Request):
	logout(Request)
	if Request.method == 'POST':
		formset = UserForm(Request.POST)
		if formset.is_valid():
			newUsr = User.objects.create_user(formset.cleaned_data['username'], formset.cleaned_data['email'], formset.cleaned_data['password'])
			user = authenticate(username=formset.cleaned_data['username'], password=formset.cleaned_data['password'])
			if user is not None:
				if user.is_active:
					login(Request, user)
			return HttpResponseRedirect('/')
	else:
		formset = UserForm()
	return render(Request, 'register.html', { 'formset' : formset.as_p(), 'search_form' : SearchForm() })

def boardView(Request, boardTag):
	currBoard = Board.objects.get(board_tag=boardTag)
	images = Image.objects.filter(board=currBoard).order_by('-upload_date')
	tags = Tag.objects.filter(board=currBoard)
	return render(Request, 'board.html', {'images' : images , 'board' : currBoard, 'tags' : tags, 'search_form' : SearchForm()})

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
	return render(Request, 'addImage.html', { 'formset' : formset.as_p() , 'boardTag' : boardTag, 'search_form' : SearchForm()})

def boardsView(Request):
	boards = Board.objects.all()
	return render(Request, 'boards.html', { 'boards' : boards , 'search_form' : SearchForm()})

def imageDetailsView(Request, boardTag, boardImageID):
	board = Board.objects.get(board_tag=boardTag)
	image = Image.objects.get(board=board, boardID=boardImageID)
	if Request.method == 'POST' and Request.user.is_authenticated():
		if 'comment_form' in Request.POST:
			formset_comments = CommentForm(Request.POST)
			if formset_comments.is_valid():
				comment = formset_comments.save(commit=False)
				comment.poster = Request.user
				comment.image = image
				comment.save()
				formset_comments = CommentForm()
			formset_tags = MissingTagsForm(image=image)
		elif 'tags_form' in Request.POST:
			formset_tags = MissingTagsForm(Request.POST, image=image)
			if formset_tags.is_valid():
				for new_tag in formset_tags.cleaned_data['tags']:
					image.tags.add(new_tag)
				formset_tags = MissingTagsForm(image=image)
			formset_comments = CommentForm()
	else:
		formset_comments = CommentForm()
		formset_tags = MissingTagsForm(image=image)
	comments = Comment.objects.filter(image=image)
	tags = image.tags.all()
	missing_tags_count = Tag.objects.filter(board=image.board).exclude(name__in = image.tags.values_list('name', flat=True)).count()
	return render(Request, 'imageDetails.html', { 'formset_comments':formset_comments.as_p(), 'formset_tags':formset_tags.as_p(), 'image':image, 'board':board, 'comments':comments, 'tags':tags, 'missing_tags':missing_tags_count, 'search_form' : SearchForm()})

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
	return render(Request, 'boardTags.html', { 'formset':formset.as_p(), 'board':board, 'tags':activeTags , 'search_form' : SearchForm()})

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
	return render(Request, 'editTag.html', { 'formset':formset.as_p(), 'board':board, 'tag':tagName , 'search_form' : SearchForm()})

def removeTagView(Request, boardTag, tagName):
	board = Board.objects.get(board_tag=boardTag)
	tag = Tag.objects.get(board=board, name=tagName)
	tag.delete()
	return HttpResponseRedirect('/board/%s/' % (boardTag))

def removeImageTagView(Request, boardTag, imageID, imageTag):
	board = Board.objects.get(board_tag=boardTag)
	image = Image.objects.get(board=board, boardID=imageID)
	removed_tag = image.tags.get(name=imageTag)
	if removed_tag:
		image.tags.remove(removed_tag)
	return HttpResponseRedirect('/board/%s/%s/' % (boardTag, imageID))

def profilesView(Request):
	users = User.objects.all().values('username')
	return render(Request, 'profiles.html', { 'users' : users , 'search_form' : SearchForm()})

def userProfileView(Request, username):
	user = User.objects.get(username=username)
	img_count = Image.objects.filter(uploader=user).count()
	comment_count = Comment.objects.filter(poster=user).count()
	return render(Request, 'userProfile.html', { 'img_count' : img_count, 'comment_count' : comment_count , 'username' : username, 'search_form' : SearchForm() })

def userUploadsView(Request, username):
	user = User.objects.get(username=username)
	images = Image.objects.filter(uploader=user)
	return render(Request, 'userUploads.html', { 'username' : username, 'images' : images , 'search_form' : SearchForm()})

def userCommentsView(Request, username):
	user = User.objects.get(username=username)
	comments = Comment.objects.filter(poster=user)
	return render(Request, 'userComments.html', { 'username' : username, 'comments' : comments , 'search_form' : SearchForm()})

def mainPageView(Request):
	image_list = Image.objects.all().order_by('-upload_date')
	paginator = Paginator(image_list, 20)
	page = Request.GET.get('page')
	try:
		images = paginator.page(page)
	except PageNotAnInteger:
		images = paginator.page(1)
	except EmptyPage:
		images = paginator.page(paginator.num_pages)
	return render(Request, 'main.html', { 'images' : images , 'search_form' : SearchForm()})

def searchView(Request):
	if Request.method == 'POST':
		formset = SearchForm(Request.POST)
		if formset.is_valid():
			searchString = formset.cleaned_data['searchString']
			searchList = filter(None ,set(searchString.split(' ')))
			includeList = []
			excludeList = []
			tagList = []
			# temp. +- analysis
			for tagString in searchList:
				if '-' in tagString:
					excludeList.append(tagString)
				else:
					includeList.append(tagString)
			# temp. tag interpret.
				if ':' in tagString:
					tagPair = tagString.split(':')
					tagPair[0] = 'board: ' + tagPair[0]
					tagPair[1] = 'tag: ' + tagPair[1]
				elif '/' in tagString:
					tagPair = []
					tagPair.append('board: ' + tagString)
				else:
					tagPair = []
					tagPair.append('tag: ' + tagString)
				tagList.append(tagPair)
	else:
		formset = SearchForm();
	return render(Request, 'search.html', { 'inc' : includeList , 'exc' : excludeList , 'tag' : tagList , 'search_form' : formset})

#TODO templates
def profileView(Request):
	return render(Request, 'profile.html')

def subscriptionsView(Request):
	return render(Request, 'subscriptions.html')
	
def inviteUsersView(Request):
	return render(Request, 'inviteUsers.html')
