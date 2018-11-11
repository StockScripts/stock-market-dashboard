# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.shortcuts import render
from .models import Search

def dashboard_view(request):
	data = {}
	if request.user.is_authenticated():
		searches = Search.objects.filter(user=request.user).order_by('-timestamp')
		for ind, search in enumerate(searches):
			data[ind] = search.query
	data = json.dumps(data)
	return render(request, 'dashboard.html', { 'data': data })

def search_view(request, query):
	if request.user.is_authenticated():
		user = request.user
		search = Search(user=user, query=query)
		search.save()
	return render(request, 'search.html', { 'query': query })
