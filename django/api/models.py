# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import pre_save
from datetime import datetime
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.





class Menu(models.Model):
	locationType = (
        ('wingold', 'Wingold'),
        ('kw', 'KW'),
        ('mon', 'Mon'),
    )

	date = models.DateField(editable=True, default=timezone.now)
	location = models.CharField(choices=locationType, max_length=100)
	title = models.TextField()
	description = models.TextField()
	caterer = models.TextField()
	#menuID = models.IntegerField(blank=True, primary_key=True)
	menuID = models.CharField(primary_key=True,editable=False, max_length=100)

	

	#class Meta:
	#	ordering = ('created',)
	def __unicode__(self):
		return str(self.menuID)

	#def save(self, *args, **kwargs):
    #    ''' On save, update timestamps '''
    #    if not self.id:
    #        self.created = timezone.now()
    #    self.modified = timezone.now()
    #    return super(User, self).save(*args, **kwargs)

def set_menu(sender, instance, **kwargs):
    ''' Trigger body '''
    for key in range(len(instance.locationType)):
    	if instance.locationType[key][0] == instance.location:
			instance.menuID = str(instance.date) + "_" +instance.locationType[key][1]
			instance.location = instance.locationType[key][1]
			break
pre_save.connect(set_menu, sender=Menu) 

class Food(models.Model):
	foodType = (
        ('halal', 'Halal'),
        ('vegan', 'Vegan'),
        ('vege', 'Vegetarian'),
    )

	name = models.CharField(max_length=100)
	menuID = models.ForeignKey(Menu, on_delete=models.CASCADE)
	cal = models.IntegerField(default=0, validators=[MinValueValidator(0)])
	description = models.TextField()
	types = models.CharField(max_length =100, choices=foodType)
	rating_counter = models.IntegerField(editable=False, default=0, validators=[MinValueValidator(0)])
	rating = models.FloatField(editable=False, default=0, validators=[MaxValueValidator(5.0), MinValueValidator(0.0) ])
	ip_list_rated = models.TextField()

	def __unicode__(self):
		return str(self.name)

