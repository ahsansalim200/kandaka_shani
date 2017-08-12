# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from random import randint

from django.contrib.auth.models import User
from django.db import models

from organisation.models import Organisation


class Base(models.Model):
	"""
	Base model for all accesscontrol models
	"""
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)
	status = models.BooleanField(default=True)

	class Meta:
		abstract = True


class AlfredUser(Base):
	"""
	Extra information of the app user will go here
	"""
	alfred_id = models.CharField(max_length=30, unique=True)
	auth_user = models.OneToOneField(User)
	organisation = models.ForeignKey(Organisation)
	superiors = models.ManyToManyField("AlfredUser", related_name='subordinates')

	def __str__(self):
		return "%s: %s" % (self.alfred_id, self.auth_user)

	@property
	def is_admin(self):
		superiors = self.superiors.all()
		return False if superiors else True
