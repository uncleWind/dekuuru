from django.db import models
from django.db.models import Max
from django.contrib.auth.models import User
from django_thumbs.db.models import ImageWithThumbsField
import os
import uuid

def imageUpload(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('upload/img', filename)

# Create your models here.
class Board(models.Model):
	name = models.CharField(max_length=50)
	board_tag = models.CharField(max_length=15, blank=False, unique=True)
	
	def __unicode__(self):
		return '/%s/ - %s' % (self.board_tag, self.name)

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
		return '%s:%s' % (self.board.name, self.name)

class Image(models.Model):
	URI = ImageWithThumbsField(upload_to=imageUpload , sizes=((200,200),))
	upload_date = models.DateTimeField(auto_now_add=True)
	uploader = models.ForeignKey(User, blank=False)
	board = models.ForeignKey(Board, blank=False)
	boardID = models.IntegerField(blank=True, null=True)
	tags = models.ManyToManyField(Tag)
	
	class Meta:
		unique_together = ('board', 'boardID',)
	
	def save(self, *args, **kwargs):
		if self.__class__.objects.filter(board=self.board).count() == 0:
			BID = 0
		else:
			BID = self.__class__.objects.filter(board=self.board).aggregate(currID=Max('boardID'))['currID'] + 1
		self.boardID = BID
		super(self.__class__, self).save(*args, **kwargs)
		
	#def __unicode__(self):
	#	return self.id
	
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
	
	class Meta:
		unique_together = ('board', 'user',)
		
	def __unicode__(self):
		return u'%s %s' % (self.board, self.user)
