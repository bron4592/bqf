from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django import forms



class search(models.Model):

	searchName = models.CharField(max_length=100)
	exchange = models.CharField(max_length=100)
	specif = models.CharField(max_length=100)
	specificEq = models.CharField(max_length=100, blank=True, default='')
	timeFrame = models.CharField(max_length=100)
	send = models.CharField(max_length=100)
	author = models.ForeignKey(User, on_delete=models.PROTECT, default=None)
	date = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-date']
		verbose_name = 'CS Search'
		verbose_name_plural = 'CS Searches'

	def __str__(self):
		return self.searchName

class watch(models.Model):

	watchName = models.CharField(max_length=100)
	specif = models.IntegerField()
	specificEq = models.CharField(max_length=100, blank=True, default='')
	timeFrame = models.CharField(max_length=100)
	retracePer = models.FloatField(blank=True, null=True)
	perRemain = models.FloatField(blank=True, null=True)
	abPer = models.FloatField(blank=True, null=True)
	volDelt = models.BooleanField(null=True)
	author = models.ForeignKey(User, on_delete=models.PROTECT, default=None)
	date = models.DateTimeField(auto_now=True)
	class Meta:
		ordering = ['-date']
		verbose_name = 'Watchlist Search'
		verbose_name_plural = 'Watchlist Searches'

	def __str__(self):
		return self.watchName

class hotlist(models.Model):

	hotName = models.CharField(max_length=100)
	maxormin = models.BooleanField(max_length=100)
	value1 = models.FloatField()
	value2 = models.FloatField()
	value3 = models.FloatField()
	value4 = models.FloatField()
	value5 = models.FloatField()
	value6 = models.FloatField()

	class Meta:
		verbose_name = 'Hotlist Search'
		verbose_name_plural = 'Hotlist Searches'

			
	def __str__(self):
		return self.hotName

