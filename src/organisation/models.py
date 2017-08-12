# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Base(models.Model):
	"""
	Base model for all accesscontrol models
	"""
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)
	status = models.BooleanField(default=True)

	class Meta:
		abstract = True


class Organisation(Base):


	organisation_id = models.CharField(max_length=30, unique=True)
	name = models.CharField(max_length=100)

	def __str__(self):
		return "%s: %s" %(self.organisation_id, self.name)
