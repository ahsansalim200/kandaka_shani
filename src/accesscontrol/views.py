# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import render



class Home(View):


	def get(self, request):
		return render(request, "login.html")


class Login(View):


	def post(self, request):
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if not user:
			context = {'error': 'Invalid username or password'}
		else:
			context = {'success': 'Congrats. You win!'}
		return render(request, "login.html", context)