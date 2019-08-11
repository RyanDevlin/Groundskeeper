from django.db import models
import datetime
from random import randint
from dateutil import tz
from urllib import request, parse
import json

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
	moisture = models.IntegerField(default=100) # Current moisture reading for the plant
	wlevel = models.IntegerField(default=100) # Current water level reading of the plant's reservoir
	wlow = models.IntegerField(default=20) # The level at which the water in the container is considered low
	wtime = models.DurationField(default=datetime.timedelta(minutes=2)) # How long to water the plant for (eg. 1 min. of running the pump)
	has_schedule = models.BooleanField(default=False) # This lets us know if this plant currently has a schedule set
	schedule = models.CharField(max_length=100) # This is the cron string used in setting the cron job for this plant
	fnotif = models.BooleanField('Low Reservoir Notifications', default=True) # Notification enable for when the water reservior needs to be refilled
	wnotif = models.BooleanField('Watering Notifications', default=True) # Notification enable for when the plant is watered
	prev_water = models.DateTimeField('Last watered') # The last time the plant was watered
	linked = models.BooleanField('Plant connected to network', default=False) # Lets us know if the web server can reach the plant node to communicate with it
	wtoday = models.BooleanField('Watered today', default=False)
	wonce = models.BooleanField('Watered at least once', default=False)
	redalert = models.BooleanField('Water is low', default=False) # Switch used for changing the color of the percentage bar on the card

	def __str__(self):
		return self.name + " the " + self.ptype + " located in the " + self.location

	def alert_send(self, message):
		# Configuration data read from config.json, this file is set up during install
		with open("config.json", "r") as file:
			data = json.load(file)

			app_key = data["app_key"] # This is the app key for the Pushed iOS app
			app_secret = data["app_secret"] # This is the app secret for the Pushed iOS app

		data = {'app_key': app_key, 'app_secret': app_secret, 'target_type': 'app', 'content': message}
		payload = parse.urlencode(data).encode()

		#print("Sending....")
		# Push the message out to the phone
		req = request.Request('https://api.pushed.co/1/push', data=payload)
		# This response processing needs to be here for some reason.
		# I think it has something to do with the asynchronisity of
		# this code versus the synchronisity of web responses
		resp = request.urlopen(req).read()
		#print(resp)

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
				self.alert_send(message)
			else:
				print("push_alert: Fill notifications are off.")
		elif(type == "watering"):
			if(self.wnotif and self.garden.wnotif_global):
				# Construct the payload
				try:
					message = self.name + ' the ' + self.ptype + ' in the ' + self.location + ' is being watered now.'
				except:
					message = self.name + ' is being watered now.'
				self.alert_send(message)
			else:
				print("push_alert: Watering notifications are off.")

		elif(type == "dont_water"):
			# Construct the payload
			try:
				message = self.name + ' the ' + self.ptype + ' in the ' + self.location + ' does not need to be watered today.'
			except:
				message = self.name + ' does not need to be watered today.'
			self.alert_send(message)
		else:
			print("ERROR push_alert: Unrecognized alert type in push_alert method.")
			print("    Type supplied: " + type)

	# This function intakes the QuerySet of all plants in the garden you want to view
	def probe(self):
		# Get the current water level and moisture reading for the plant
		self.wlevel = randint(0, 100)
		self.moisture = randint(0, 100)

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
		"""
		if(not self.linked):
			print("ERROR water: Plant not linked!")

		else:
			# Water the plant
			"""

		"""
		# Auto-detect zones:
		from_zone = tz.tzutc()
		to_zone = tz.tzlocal()

		utc = datetime.datetime.utcnow()

		# Tell the datetime object that it's in UTC time zone since 
		# datetime objects are 'naive' by default
		utc = utc.replace(tzinfo=from_zone)
		"""

		# Convert time zone
		#self.prev_water = utc.astimezone(to_zone)
		self.push_alert("watering")
		self.prev_water = datetime.datetime.now()
		self.wonce = True
		self.save()








