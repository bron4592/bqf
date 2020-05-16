from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView
from . forms import newSearch, newWatch, newHot
from . models import search, watch
from structures.breakout import breakout
from django.contrib.auth.mixins import LoginRequiredMixin
from . watcher import querys, hotRSI, rsiQuery, inHot
from django.core.management import call_command

@login_required(login_url='/login/')
def home(request):
	context = {
		'hots':rsiQuery()
	}
	return render(request, 'home/home.html', context)

@login_required(login_url='/login/')
def search(request):
	if request.method == 'POST':
		form = newSearch(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.author = request.user
			instance.save()
			messages.success(request, f'New Search Successfully Added!')
			return redirect('bqf-home')
	else:
		form = newSearch()
	return render(request, 'home/search.html', {'form':form})

@login_required(login_url='/login/')
def watchlist(request):
	context = {
		'watches':querys()
	}
	return render(request, 'home/watch_list.html', context)

class watchlistView(LoginRequiredMixin, ListView):
	login_url = '/login/'
	model = watch
	context_object_name = 'watches'
	ordering = ['-date']
'''
class watchlistDetailView(LoginRequiredMixin, DetailView):
	login_url = '/login/'
	model = watch
'''
@login_required(login_url='/login/')
def trades(request):
	return render(request, 'home/trades.html')

@login_required(login_url='/login/')
def createWatch(request):
	if request.method == 'POST':
		form = newWatch(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.author = request.user
			instance.save()
			querys()
			messages.success(request, f'New Watchlist Successfully Added!')
			return redirect('bqf-home')
	else:
		form = newWatch()
	return render(request, 'home/createWatch.html', {'form':form})

@login_required(login_url='/login/')
def hotlist(request):
	context = {
		'hots':rsiQuery()
	}
	
	return render(request, 'home/hotlist.html', context)

@login_required(login_url='/login/')
def createhotlist(request):
	if request.method == 'POST':
		form = newHot(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.author = request.user
			instance.save()
			querys()
			messages.success(request, f'New Hotlist Successfully Added!')
			return redirect('bqf-home')
	else:
		form = newHot()
	return render(request, 'home/createhotlist.html', {'form':form})
