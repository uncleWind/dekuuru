from django.shortcuts import render
from dekuuro.forms import *
from dekuuro.models import *
from django.http import HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login
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
	images = Image.objects.filter(board=currBoard).order_by('-upload_date')
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
	return render(Request, 'imageDetails.html', { 'formset_comments':formset_comments.as_p(), 'formset_tags':formset_tags.as_p(), 'image':image, 'board':board, 'comments':comments, 'tags':tags, 'missing_tags':missing_tags_count})

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

def removeImageTagView(Request, boardTag, imageID, imageTag):
	board = Board.objects.get(board_tag=boardTag)
	image = Image.objects.get(board=board, boardID=imageID)
	removed_tag = image.tags.get(name=imageTag)
	if removed_tag:
		image.tags.remove(removed_tag)
	return HttpResponseRedirect('/board/%s/%s/' % (boardTag, imageID))

#TODO templates
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
	return render(Request, 'main.html', { 'images' : images })

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
