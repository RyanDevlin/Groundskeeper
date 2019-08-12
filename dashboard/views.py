from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from dashboard.models import Garden, Plant
from random import randint
from datetime import datetime
from django.utils import timezone
import pytz
from django.conf import settings
from django import forms
from django.urls import reverse
from dashboard.plant_backend import chart_backend

from .forms import PlantForm, SettingsForm
from django.contrib.auth.decorators import login_required

from collections import OrderedDict

# Include the `fusioncharts.py` file that contains functions to embed the charts.
from dashboard.fusioncharts import FusionCharts

# NOTE: Notice that the code here is hardcoded to only work with plants from the first garden
# The ability to have multiple gardens is a feature to be added in the future

@login_required()
def dash_index(request): 
	garden = Garden.objects.get(garden_name="NYC Apartment")
	plants = garden.plant_set.all() # This pulls up a QuerySet of all the plants in our garden

	# Update the database with the correct plant water level and moisture readings
	for plant in plants:
		plant.probe()
	# We need to query the updated database again to create the proper context
	garden = Garden.objects.get(garden_name="NYC Apartment")
	plants = garden.plant_set.all()

	context = {
		'plants': plants,
		'garden': garden
	}

	# Probe the plants to get the current status of each

	return render(request, 'dashboard/dash_index.html', context)

@login_required()
def plant_detail(request, pk):
	garden =Garden.objects.get(garden_name="NYC Apartment")
	plants = garden.plant_set.all() # Pull up the requested plant data
	plant = get_object_or_404(plants, pk=pk)

	column2D = plant.chart_constructor()
	if(column2D == None):
		raise ValueError('Incorrect useage of chart_backend() in plant_detail in views.py')

	context = {
		'plant': plant,
		'garden': garden,
		'output': column2D.render()
	}
	return render(request, 'dashboard/plant_detail.html', context)

@login_required()
def plant_add(request, gname):
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = PlantForm(request.POST)
		form.as_ul()
		# check whether it's valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required
			g = Garden.objects.get(garden_name=gname)
			t_name = form.cleaned_data['name']
			t_type = form.cleaned_data['ptype']
			t_loc = form.cleaned_data['location']
			t_fnotif = form.cleaned_data['fnotif']
			t_wnotif = form.cleaned_data['wnotif']
			#settings.TIME_ZONE
			g.plant_set.create(name=t_name, ptype=t_type, location=t_loc, fnotif=t_fnotif, wnotif=t_wnotif, prev_water=datetime.now())

			# redirect to a new URL:
			return HttpResponseRedirect(reverse('dash_index')) # Bring us back to the main page

	# if a GET (or any other method) we'll create a blank form
	else:
		form = PlantForm()
		form.as_ul()

	garden = get_object_or_404(Garden, garden_name=gname)
	context = {
		'form': form,
		'garden': garden
	}
	return render(request, 'dashboard/plant_add.html', context)

@login_required()
def plant_delete(request, pk):
	garden =Garden.objects.get(garden_name="NYC Apartment")
	plants = garden.plant_set.all() # Pull up the requested plant data
	plant = get_object_or_404(plants, pk=pk)
	plant.delete()
	return HttpResponseRedirect(reverse('dash_index'))

@login_required()
def plant_water(request, pk):
	garden =Garden.objects.get(garden_name="NYC Apartment")
	plants = garden.plant_set.all() # Pull up the requested plant data
	plant = get_object_or_404(plants, pk=pk)
	plant.water()
	return HttpResponseRedirect(reverse('dash_index'))

@login_required()
def settings_page(request, pk):
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		garden = Garden.objects.get(pk=pk)
		form = SettingsForm(request.POST, instance=garden)
		form.as_ul()
		# check whether it's valid:
		if form.is_valid():
			form.save()

			# redirect to a new URL:
			return HttpResponseRedirect(reverse('dash_index')) # Bring us back to the main page

	# if a GET (or any other method) we'll create a blank form
	else:
		garden = Garden.objects.get(pk=pk)
		form = SettingsForm(instance=garden)
		form.as_ul()

	garden = get_object_or_404(Garden, pk=pk)
	context = {
		'form': form,
		'garden': garden
	}
	return render(request, 'dashboard/settings_page.html', context)


