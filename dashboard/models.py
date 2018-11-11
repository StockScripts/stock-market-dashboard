# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

from datetime import datetime

class Search(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	query = models.CharField(max_length=255)
	timestamp = models.DateTimeField(default=datetime.now)

	class Meta:
		verbose_name_plural = "Searches"

	def __str__(self):
		return self.query
