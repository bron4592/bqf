from django.db import models
from django.utils import timezone
from django import forms



class struct(models.Model):

	idCode = models.CharField(max_length=100)
	date = models.DateTimeField()
	exchange = models.CharField(max_length=100)
	eqName = models.CharField(max_length=100)
	timeFrame = models.CharField(max_length=100)
	bVol = models.IntegerField()
	takeVol = models.IntegerField()
	volDelt = models.IntegerField()
	retracePer = models.FloatField()
	perRemain = models.FloatField()
	direction = models.CharField(max_length=100)
	abPer = models.FloatField()
	abLength = models.FloatField()
	c = models.FloatField()
	b = models.FloatField()
	takeout = models.FloatField()
	valid = models.BooleanField(default=True)
	newTake = models.BooleanField(default=False)
	class Meta:
		ordering = ['-date']
		verbose_name = 'Confirmed Structure'
		verbose_name_plural = 'Confirmed Structures'

	def __str__(self):
		return self.eqName

class trade(models.Model):
	eqName = models.CharField(max_length=100)
	date = models.DateTimeField()
	childtime = models.CharField(max_length=100)
	parTime = models.CharField(max_length=100)
	indicator = models.CharField(max_length=100)
	current = models.FloatField()
	thresh = models.FloatField(blank=True)
	direction = models.CharField(max_length=100)
	valid = models.BooleanField(default=True)

	class Meta:
		ordering = ['-date']
		verbose_name = 'RSI-Watchlist Structure'
		verbose_name_plural = 'RSI-Watchlist Structures'
	def __str__(self):
		return self.eqName

class invalid(models.Model):
	idCode = models.CharField(max_length=100)
	date = models.DateTimeField()
	exchange = models.CharField(max_length=100)
	eqName = models.CharField(max_length=100)
	timeFrame = models.CharField(max_length=100)
	bVol = models.IntegerField()
	takeVol = models.IntegerField()
	volDelt = models.IntegerField()
	retracePer = models.FloatField()
	perRemain = models.FloatField()
	direction = models.CharField(max_length=100)
	abPer = models.FloatField()
	abLength = models.FloatField()
	c = models.FloatField()
	takeout = models.FloatField()
	valid = models.BooleanField(default=False)
	class Meta:
		verbose_name = 'Invalid Structure'
		verbose_name_plural = 'Invalid Structures'
			
		
'''
Date of Occurrence
Security Type
Security Name
Time Frame
B-Point Bar  Volume
Takeout Bar Volume
Volume Delta
Retracement %
Potential Return %
% of Extension Left to Achieve
'''