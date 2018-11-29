# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import StockFilterForm, UserSettingsForm
from .models import Profile, Search
from .utils import (
	fetch_data,
	fetch_news,
	update_database,
	TIME_INTERVALS,
	FUNCTIONS,
)

def dashboard_view(request):
	data = {}
	if request.user.is_authenticated():
		searches = Search.objects.filter(user=request.user).order_by('-timestamp')
		for ind, search in enumerate(searches):
			data[ind] = search.query
		value = Profile.objects.filter(user=request.user).values('refresh_time')[0]['refresh_time']
	else:
		value = 60000
	if request.method == 'POST':
		form = StockFilterForm(request.POST)
		if form.is_valid():
			stock = request.POST.get('stock', '')
			interval = int(request.POST.get('interval', ''))
			attribute = request.POST.get('attribute', '')
	else:
		form = StockFilterForm()
		stock = 'AAPL'
		interval = 0
		attribute = 'opening'
	stats = fetch_data(stock, interval)
	data = json.dumps(data)
	return render(request, 'dashboard.html', {
		'data': data,
		'stats': stats,
		'val': value,
		'form': form,
		'series': interval,
		'attr': attribute,
	})

@login_required(login_url='/login')
def profile_view(request):
	if request.method == 'POST':
		form = UserSettingsForm(request.POST)
		if form.is_valid():
			refresh_time = request.POST.get('refresh_time', '')
			Profile.objects.filter(user=request.user).update(refresh_time=refresh_time)
			value = refresh_time
	else:
		value = Profile.objects.filter(user=request.user).values('refresh_time')[0]['refresh_time']
	form = UserSettingsForm()
	return render(request, 'profile.html', { 'form': form, 'val': value })

def refresh_view(request, series):
	update_database(int(series))
	return redirect('/')

def search_view(request, query):
	if request.user.is_authenticated():
		user = request.user
		search = Search(user=user, query=query)
		search.save()
	news = fetch_news(query)
	return render(request, 'search.html', { 'query': query, 'news': news })
