from random import randint
from datetime import datetime
from collections import OrderedDict
import json
from urllib import request, parse
from celery import shared_task

# Include the `fusioncharts.py` file that contains functions to embed the charts.
from dashboard.fusioncharts import FusionCharts


def chart_backend(plant):
	#Chart data is passed to the `dataSource` parameter, like a dictionary in the form of key-value pairs.
	dataSource = OrderedDict()

	# The `chartConfig` dict contains key-value pairs of data for chart attribute
	chartConfig = OrderedDict()
	chartConfig["caption"] = "Live Moisture Readings for " + plant.name
	chartConfig["subCaption"] = "Moisture Data Sampled at a Rate of One Measurement Per Hour"
	chartConfig["xAxisName"] = "Time of Day"
	chartConfig["yAxisName"] = "Moisture (%)"
	chartConfig["numberSuffix"] = "%"
	chartConfig["theme"] = "fusion"
	chartConfig["labelStep"] = "2"
	chartConfig["labelDisplay"] = "rotate"
	chartConfig["slantLabel"] = "1"

	# Pull up the plant moisture data
	moisture = plant.moisture.split(";")
	chartData = OrderedDict()
	times = ["12:00am", "1:00am", "2:00am", "3:00am",
			 "4:00am", "5:00am", "6:00am", "7:00am",
			 "8:00am", "9:00am", "10:00am", "11:00am",
			 "12:00pm", "1:00pm", "2:00pm", "3:00pm",
			 "4:00pm", "5:00pm", "6:00pm", "7:00pm",
			 "8:00pm", "9:00pm", "10:00pm", "11:00pm"]
	
	i = 0
	now = datetime.now()
	for time in times:
		print(i)
		if(i > now.hour):
			chartData[time] = None # This is for data that we dont have yet because it will be measured lated today
		else:
			chartData[time] = moisture[i]
		i += 1

	dataSource["chart"] = chartConfig
	dataSource["data"] = []

	# Convert the data in the `chartData` array into a format that can be consumed by FusionCharts.
	#The data for the chart should be in an array wherein each element of the array
	#is a JSON object# having the `label` and `value` as keys.

	#Iterate through the data in `chartData` and insert into the `dataSource['data']` list.
	for key, value in chartData.items():
		data = {}
		data["label"] = key
		data["value"] = value
		dataSource["data"].append(data)

	# Create an object for the column 2D chart using the FusionCharts class constructor
	# The chart data is passed to the `dataSource` parameter.
	return FusionCharts("spline", "myFirstChart", "100%", "100%", "myFirstchart-container", "json", dataSource)

# Use the shared_task decorator here to allow celery to run this task in the background
@shared_task
def alert_send(message):
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

