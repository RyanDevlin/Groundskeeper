from random import randint
from datetime import datetime
from dashboard.models import Plant
from collections import OrderedDict

# Include the `fusioncharts.py` file that contains functions to embed the charts.
from dashboard.fusioncharts import FusionCharts


def chart_backend(plant):
	if(not isinstance(plant, Plant)):
		print("ERROR chart_backend: This function only instakes objects of type Plant as defined in the dashboard models.")
		return None

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
	times = ["12:00am", "1:00am", "2:00am", "3:00am", "4:00am", "5:00am", "6:00am", "7:00am", "8:00am", "9:00am", "10:00am", "11:00am", "12:00pm", "1:00pm", "2:00pm", "3:00pm", "4:00pm", "5:00pm", "6:00pm", "7:00pm", "8:00pm", "9:00pm", "10:00pm", "11:00pm"]
	
	i =0
	for time in times:
		chartData[time] = moisture[i]
		i += 1

	dataSource["chart"] = chartConfig
	dataSource["data"] = []

	# Convert the data in the `chartData`array into a format that can be consumed by FusionCharts.
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

