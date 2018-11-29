# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from datetime import datetime

class Search(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	query = models.CharField(max_length=255)
	timestamp = models.DateTimeField(default=datetime.now)

	class Meta:
		verbose_name_plural = "Searches"

	def __str__(self):
		return self.query

class Profile(models.Model):
	REFRESH_RATES = (
		(60000, '1 min'),
		(180000, '3 min'),
		(600000, '10 min'),
		(1800000, '30 min'),
	)
	user = models.OneToOneField(
		User,
		on_delete=models.CASCADE,
		primary_key=True,
	)
	refresh_time = models.IntegerField(
		choices=REFRESH_RATES,
		default=60000,
	)


class Stock(models.Model):
	name = models.CharField(max_length=255)

	def __str__(self):
		return self.name

class StockDailyFive(models.Model):
	name = models.ForeignKey(Stock, on_delete=models.CASCADE)
	opening = models.DecimalField(max_digits=20,decimal_places=8)
	closing = models.DecimalField(max_digits=20,decimal_places=8)
	high = models.DecimalField(max_digits=20,decimal_places=8)
	low = models.DecimalField(max_digits=20,decimal_places=8)
	volume = models.DecimalField(max_digits=20,decimal_places=8)
	timestamp = models.DateTimeField()

	def __str__(self):
		return '%s %s' % (self.name.name, self.timestamp)

class StockDailyFifteen(models.Model):
	name = models.ForeignKey(Stock, on_delete=models.CASCADE)
	opening = models.DecimalField(max_digits=20,decimal_places=8)
	closing = models.DecimalField(max_digits=20,decimal_places=8)
	high = models.DecimalField(max_digits=20,decimal_places=8)
	low = models.DecimalField(max_digits=20,decimal_places=8)
	volume = models.DecimalField(max_digits=20,decimal_places=8)
	timestamp = models.DateTimeField()

	def __str__(self):
		return '%s %s' % (self.name.name, self.timestamp)

class StockDailyThirty(models.Model):
	name = models.ForeignKey(Stock, on_delete=models.CASCADE)
	opening = models.DecimalField(max_digits=20,decimal_places=8)
	closing = models.DecimalField(max_digits=20,decimal_places=8)
	high = models.DecimalField(max_digits=20,decimal_places=8)
	low = models.DecimalField(max_digits=20,decimal_places=8)
	volume = models.DecimalField(max_digits=20,decimal_places=8)
	timestamp = models.DateTimeField()

	class Meta:
		verbose_name_plural = "Stock daily thirties"

	def __str__(self):
		return '%s %s' % (self.name.name, self.timestamp)

class StockWeekly(models.Model):
	name = models.ForeignKey(Stock, on_delete=models.CASCADE)
	opening = models.DecimalField(max_digits=20,decimal_places=8)
	closing = models.DecimalField(max_digits=20,decimal_places=8)
	high = models.DecimalField(max_digits=20,decimal_places=8)
	low = models.DecimalField(max_digits=20,decimal_places=8)
	volume = models.DecimalField(max_digits=20,decimal_places=8)
	timestamp = models.DateTimeField()

	class Meta:
		verbose_name_plural = "Stock weekly"

	def __str__(self):
		return '%s %s' % (self.name.name, self.timestamp)

class StockMonthly(models.Model):
	name = models.ForeignKey(Stock, on_delete=models.CASCADE)
	opening = models.DecimalField(max_digits=20,decimal_places=8)
	closing = models.DecimalField(max_digits=20,decimal_places=8)
	high = models.DecimalField(max_digits=20,decimal_places=8)
	low = models.DecimalField(max_digits=20,decimal_places=8)
	volume = models.DecimalField(max_digits=20,decimal_places=8)
	timestamp = models.DateTimeField()

	class Meta:
		verbose_name_plural = "Stock monthly"

	def __str__(self):
		return '%s %s' % (self.name.name, self.timestamp)

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
	if created:
		profile = Profile(user=instance)
		profile.save()
