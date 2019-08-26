from django.db import models
import datetime
from random import randint
from dateutil import tz
from urllib import request, parse
import json
from dashboard.plant_backend import alert_send, chart_backend
from django.utils import timezone
from crontab import CronTab
from django.conf import settings

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

class Garden(models.Model):
	garden_name = models.CharField(max_length=100)
	fnotif_global = models.BooleanField('Low Reservoir Notifications', default=True) # Notification enable for when the water reservior needs to be refilled
	wnotif_global = models.BooleanField('Watering Notifications', default=True) # Notification enable for when the plant is watered	

	def __str__(self):
		return self.garden_name

class Plant(models.Model):
	garden = models.ForeignKey(Garden, on_delete=models.CASCADE) # Many to one mapping of every plant to a garden
	name = models.CharField(max_length=100) # A unique identifier for the plant, for instance: Oscar
	ptype = models.CharField(max_length=100) # Type of the plant(eg. snake_plant)
	location = models.CharField(max_length=100) # Location of the plant (bedroom, livingroom, etc.)
	moisture = models.CharField(max_length=100, default="098;094;092;090;082;080;064;060;098;094;092;090;082;080;064;060;098;094;092;090;082;080;064;060") # Past 24 hours of moisture readings for the plant
	wlevel = models.IntegerField(default=100) # Current water level reading of the plant's reservoir
	wlow = models.IntegerField(default=20) # The level at which the water in the container is considered low
	wtime = models.DurationField(default=datetime.timedelta(minutes=2)) # How long to water the plant for (eg. 1 min. of running the pump)
	has_schedule = models.BooleanField(default=False) # This lets us know if this plant currently has a schedule set
	schedule_freq = models.CharField('Scheduled watering frequency', max_length=3, choices=FREQ, default='1')
	schedule_time = models.CharField('Scheduled watering time', max_length=2, choices=TIME, default='19')
	schedule_start = models.CharField('Scheduled watering start', max_length=3, choices=START, default='MON')
	fnotif = models.BooleanField('Low Reservoir Notifications', default=True) # Notification enable for when the water reservior needs to be refilled
	wnotif = models.BooleanField('Watering Notifications', default=True) # Notification enable for when the plant is watered
	prev_water = models.DateTimeField('Last watered') # The last time the plant was watered
	linked = models.BooleanField('Plant connected to network', default=False) # Lets us know if the web server can reach the plant node to communicate with it
	wtoday = models.BooleanField('Watered today', default=False)
	wonce = models.BooleanField('Watered at least once', default=False)
	redalert = models.BooleanField('Water is low', default=False) # Switch used for changing the color of the percentage bar on the card

	def __str__(self):
		return self.name + " the " + self.ptype + " located in the " + self.location

	#########################################################################
	# This method intakes a type of alert and pushes the alert to my iPhone.
	#########################################################################
	def push_alert(self, type):
		if(type == "water_low"):
			if(self.fnotif and self.garden.fnotif_global):
				# Construct the payload
				try:
					message = self.name + ' the ' + self.ptype + ' in the ' + self.location + ' has a low water reservoir!'
				except:
					message = self.name + ' has a low water reservoir!'
				alert_send.delay(message)
			else:
				print("push_alert: Fill notifications are off.")
		elif(type == "watering"):
			if(self.wnotif and self.garden.wnotif_global):
				# Construct the payload
				try:
					message = self.name + ' the ' + self.ptype + ' in the ' + self.location + ' is being watered now.'
				except:
					message = self.name + ' is being watered now.'
				alert_send.delay(message)
			else:
				print("push_alert: Watering notifications are off.")

		elif(type == "dont_water"):
			# Construct the payload
			try:
				message = self.name + ' the ' + self.ptype + ' in the ' + self.location + ' does not need to be watered today.'
			except:
				message = self.name + ' does not need to be watered today.'
			alert_send.delay(message)
		else:
			print("ERROR push_alert: Unrecognized alert type in push_alert method.")
			print("    Type supplied: " + type)

	# This function intakes the QuerySet of all plants in the garden you want to view
	def probe(self):
		# Get the current water level and moisture reading for the plant
		self.wlevel = randint(0, 100)

		# Check if the plant was watered today
		if(self.prev_water.date() == datetime.datetime.utcnow().date()): # For some inane reason I don't feel like figuring out, I need to keep the current datetime in utc becasue the prev_water time is in utc so to compare them they must be the same. No clue why prev_water is working that way, but who cares? [famous last words]
			self.wtoday = True
		else:
			self.wtoday = False

		if(self.wlevel < 50):
			self.redalert = True
		else:
			self.redalert = False
		self.save()

	def water(self):
		# Check for linkage here
		self.push_alert("watering")
		self.prev_water = timezone.now()
		self.wonce = True
		self.save()

	def chart_constructor(self):
		return chart_backend(self)

	def update_schedule(self):
		with open(settings.BASE_DIR + "/config.json", "r") as file:
			data = json.load(file)

			user = data["user"] # Username for the machine running this code
			root = data["root"] # Project root, notice it must end in a '/'
			python3_path = data["python3_path"]

		cron_string = self.create_cron_string()
		print("CRON: " + cron_string)

		if(self.has_schedule):
			try:
				my_cron = CronTab(user=user)
				for job in my_cron:
					if(job.comment == str(self.pk) + "_water_schedule"):
						job.setall(cron_string)
						my_cron.write()
						self.schedule = cron_string
			except:
				print("ERROR set_schedule: Invalid cron value in set_schedule method")
				exit()
		else:
			try:
				my_cron = CronTab(user=user)
				comment = str(self.pk) + "_water_schedule"
				command = python3_path + " " + root + "manage.py water " + str(self.pk)
				job = my_cron.new(command=command, comment=comment)
				job.setall(cron_string)
				 
				my_cron.write()
				self.schedule = cron_string
				self.has_schedule = True
				self.save()
			except:
				print("ERROR set_schedule: Invalid cron value in set_schedule method")
				exit()
	#########################################################################
	# This method deletes the schedule for the watering of the plant
	#########################################################################
	def delete_schedule(self):
		with open(settings.BASE_DIR + "/config.json", "r") as file:
			data = json.load(file)

			user = data["user"] # Username for the machine running this code

		if(self.has_schedule == False):
			print("ERROR delete_schedule: No schedule exists delete_schedule method")

		my_crons = CronTab(user=user)
		for job in my_crons:
			if(job.comment == str(self.pk) + "_water_schedule"):
				my_crons.remove(job)
				my_crons.write()
				self.schedule = None
				self.has_schedule = False


	def create_cron_string(self):
		now = timezone.now()
		select = {
			'1': '* * *',
			'2': '*/2 * *',
			'week': '*/1 * ' + str(self.schedule_start),
			'month': str(now.day) + ' */1 *'
		}

		# Cron translations for the time
		time_sel = {  
		    '1': '0 0 ',
		    '2': '30 0 ',
		    '3': '0 1 ',
		    '4': '30 1 ',
		    '5': '0 2 ',
		    '6': '30 2 ',
		    '7': '0 3 ',
		    '8': '30 3 ',
		    '9': '0 4 ',
		    '10': '30 4 ',
		    '11': '0 5 ',
		    '12': '30 5 ',
		    '13': '0 6 ',
		    '14': '30 6 ',
		    '15': '0 7 ',
		    '16': '30 7 ',
		    '17': '0 8 ',
		    '18': '30 8 ',
		    '19': '0 9 ',
		    '20': '30 9 ',
		    '21': '0 10 ',
		    '22': '30 10 ',
		    '23': '0 11 ',
		    '24': '30 11 ',
		    '25': '0 12 ',
		    '26': '30 12 ',
		    '27': '0 13 ',
		    '28': '30 13 ',
		    '29': '0 14 ',
		    '30': '30 14 ',
		    '31': '0 15 ',
		    '32': '30 15 ',
		    '33': '0 16 ',
		    '34': '30 16 ',
		    '35': '0 17 ',
		    '36': '30 17 ',
		    '37': '0 18 ',
		    '38': '30 18 ',
		    '39': '0 19 ',
		    '40': '30 19 ',
		    '41': '0 20 ',
		    '42': '30 20 ',
		    '43': '0 21 ',
		    '44': '30 21 ',
		    '45': '0 22 ',
		    '46': '30 22 ',
		    '47': '0 23 ',
		    '48': '30 23 ',
		}
		cron_string = time_sel[self.schedule_time] + select[self.schedule_freq]
		return cron_string



