from random import randint
from datetime import datetime

# This function intakes the QuerySet of all plants in the garden you want to view
def plant_probe(plants):
	try:
		# Get the current water level and moisture reading for the plant
		for plant in plants:
			plant.wlevel = randint(0, 100)
			plant.moisture = randint(0, 100)

			# Check if the plant was watered today
			if(plant.prev_water.date() == datetime.now().date()):
				print("HERE")
				plant.wtoday = True
			else:
				print("HERE")
				plant.wtoday = False
			plant.save()
	except:
		print("ERROR plant_probe: the argument passed to plant_probe must be a QuerySet of plants.")


# This function waters the plant
def plant_probe(plants):
	return