from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import struct
from .breakout import remove, multiValid, breakout



@login_required(login_url='/login/')
def database(request):
	context = {
		'structure': struct.objects.all()
	}

	return render(request, 'structures/database.html', context)
