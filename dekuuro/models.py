from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Board(models.Model):
	name = models.CharField(max_length=50)
	board_tag = models.CharField(max_length=15, blank=False, unique=True)

class BoardSubscription(models.Model):
	user = models.ForeignKey(User, blank=False)
	board = models.ForeignKey(Board, blank=False)
	
	class Meta:
		unique_together = ('user', 'board',)
	
class Tag(models.Model):
	board = models.ForeignKey(Board)
	name = models.CharField(max_length=30, blank=False)
	
	class Meta:
		unique_together = ('board', 'name',)
	
	def __unicode__(self):
		return u'%s:%s' (self.board.name, self.name)

class Image(models.Model):
	URI = models.FileField(max_length=400, blank=False)
	thumb_URI = models.FileField(max_length=400)
	upload_date = models.DateTimeField(auto_now_add=True)
	uploader = models.ForeignKey(User, blank=False)
	board = models.ForeignKey(Board, blank=False)
	boardID = models.IntegerField(blank=False)
	tags = models.ManyToManyField(Tag)
	
class Comment(models.Model):
	poster = models.ForeignKey(User, blank=False)
	image = models.ForeignKey(Image, blank=False)
	content = models.TextField(max_length=500, blank=False)
	post_date = models.DateTimeField(auto_now_add=True)
	
class Profile(models.Model):
	user = models.ForeignKey(User, blank=False)
	name = models.CharField(max_length=50, blank=False)
	filtered_tags = models.ManyToManyField(Tag)
	
class BoardUsers(models.Model):
	PRIVILEDGES = (
		('ADM', 'Admin'),
		('MOD', 'Moderator'),
		('UPL', 'Uploader'),
		('STD', 'Standard'),
	)
	board = models.ForeignKey(Board, blank=False)
	user = models.ForeignKey(User, blank=False)
	priviledge_level = models.CharField(max_length=3, choices=PRIVILEDGES, blank=False)
