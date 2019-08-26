from django import forms
from dashboard.models import Garden, Plant
import datetime

FREQ = (  
    ('1', 'day'),
    ('2', 'other day'),
    ('week', 'week'),
    ('month', 'month from today'),
)

TIME = (  
    ('1', '12:00am'),
    ('2', '12:30am'),
    ('3', '1:00am'),
    ('4', '1:30am'),
    ('5', '2:00am'),
    ('6', '2:30am'),
    ('7', '3:00am'),
    ('8', '3:30am'),
    ('9', '4:00am'),
    ('10', '4:30am'),
    ('11', '5:00am'),
    ('12', '5:30am'),
    ('13', '6:00am'),
    ('14', '6:30am'),
    ('15', '7:00am'),
    ('16', '7:30am'),
    ('17', '8:00am'),
    ('18', '8:30am'),
    ('19', '9:00am'),
    ('20', '9:30am'),
    ('21', '10:00am'),
    ('22', '10:30am'),
    ('23', '11:00am'),
    ('24', '11:30am'),
    ('25', '12:00pm'),
    ('26', '12:30pm'),
    ('27', '1:00pm'),
    ('28', '1:30pm'),
    ('29', '2:00pm'),
    ('30', '2:30pm'),
    ('31', '3:00pm'),
    ('32', '3:30pm'),
    ('33', '4:00pm'),
    ('34', '4:30pm'),
    ('35', '5:00pm'),
    ('36', '5:30pm'),
    ('37', '6:00pm'),
    ('38', '6:30pm'),
    ('39', '7:00pm'),
    ('40', '7:30pm'),
    ('41', '8:00pm'),
    ('42', '8:30pm'),
    ('43', '9:00pm'),
    ('44', '9:30pm'),
    ('45', '10:00pm'),
    ('46', '10:30pm'),
    ('47', '11:00pm'),
    ('48', '11:30pm'),
)

START = (  
    ('MON', 'Monday'),
    ('TUE', 'Tuesday'),
    ('WED', 'Wednesday'),
    ('THU', 'Thursday'),
    ('FRI', 'Friday'),
    ('SAT', 'Saturday'),
    ('SUN', 'Sunday'),
)

class PlantForm(forms.Form):
	name = forms.CharField(label='Plant name (eg. Carlitos)', max_length=100)
	ptype = forms.CharField(label='Plant type (eg. Snake Plant)', max_length=100)
	location = forms.CharField(label='Plant location (eg. kitchen)', max_length=100)
	wtime = forms.DurationField(label='Watering duration (hr : min : sec)', initial=datetime.timedelta(minutes=2))
	schedule_freq = forms.ChoiceField(label='Water this plant every', required=True, choices=FREQ)
	schedule_time = forms.ChoiceField(label='At', required=True, choices=TIME)
	schedule_start = forms.ChoiceField(label='On (only if watering every week)', required=True, choices=START)
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
		fields = ['name', 'ptype', 'location', 'wtime', 'fnotif', 'wnotif', 'schedule_freq', 'schedule_time', 'schedule_start']
		labels = {
			"name": "Plant name (eg. Carlitos)",
			"ptype": "Plant type (eg. Cactus)",
			"location": "Plant location (eg. Kitchen)",
			"wtime": "Watering duration (hr : min : sec)",
			"fnotif": "Notifications when this plant's water reservoir is low",
			"wnotif": "Notifications when this plant is watered",
			"schedule_freq": "Water this plant every",
			"schedule_time": "At",
			"schedule_start": "On (only if watering every week)"
		}

	def clean_name(self):
		name = self.cleaned_data.get('name')
		if(Plant.objects.filter(name=name).exclude(pk=self.instance.pk).exists()):
			raise forms.ValidationError(u'There is already a plant named "%s"' % name)
		return name











