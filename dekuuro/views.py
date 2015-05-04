from django.shortcuts import render
from dekuuro.forms import *
from dekuuro.models import *
from django.http import HttpResponseRedirect

# Create your views here.

def testView(Request):
	if Request.method == 'POST':
		formset = BoardForm(Request.POST)
		if formset.is_valid():
			return HttpResponseRedirect('')
	else:
		formset = BoardForm()
	return render(Request, 'test.html', { 'formset' : formset })
