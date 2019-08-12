from django import forms
from dashboard.models import Garden, Plant

class PlantForm(forms.Form):
	name = forms.CharField(label='Plant name (eg. Carlitos)', max_length=100)
	ptype = forms.CharField(label='Plant type (eg. Snake Plant)', max_length=100)
	location = forms.CharField(label='Plant location (eg. kitchen)', max_length=100)
	fnotif = forms.BooleanField(label='Notifications when the water reservoir is low', initial=True, required=False) # Notification enable for when the water reservior needs to be refilled
	wnotif = forms.BooleanField(label='Notifications when the plant is watered', initial=True, required=False) # Notification enable for when the plant is watered

	def clean_name(self):
		name = self.cleaned_data.get('name')

		if Plant.objects.filter(name=name).exists():
			raise forms.ValidationError(u'There is already a plant named "%s"' % name)
		return name

class SettingsForm(forms.ModelForm):

	class Meta:
		model = Garden
		fields = ['garden_name', 'fnotif_global', 'wnotif_global']

	def clean_garden_name(self):
		garden_name = self.cleaned_data.get('garden_name')
		if(Garden.objects.filter(garden_name=garden_name).exclude(pk=self.instance.pk).exists()):
			raise forms.ValidationError(u'There is already a garden named "%s"' % garden_name)
		return garden_name

class PlantSettingsForm(forms.ModelForm):

	class Meta:
		model = Plant
		fields = ['name', 'ptype', 'location', 'schedule', 'wtime', 'fnotif', 'wnotif']
		labels = {
			"name": "Plant name (eg. Carlitos)",
			"ptype": "Plant type (eg. Cactus)",
			"location": "Plant location (eg. Kitchen)",
			"schedule": "Watering schedule",
			"wtime": "Watering time (hr : min : sec)",
			"fnotif": "Notifications when this plant's water reservoir is low",
			"wnotif": "Notifications when this plant is watered"
		}

	def clean_name(self):
		name = self.cleaned_data.get('name')
		if(Plant.objects.filter(name=name).exclude(pk=self.instance.pk).exists()):
			raise forms.ValidationError(u'There is already a plant named "%s"' % name)
		return name