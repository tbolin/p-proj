# -*- coding: UTF-8 -*-

# P-uppgift
# errands

# Contains functions representing the 
# various services a facility can provide

# If a facility can provide a service,
# attach the service function to the facility instance

# class Service:
	# Template for services
	# start_str = ""
	# name_str = ""
	# done_str = ""
	
	# def __init__(self, facility=None, time=1):
		# self.facility = facility
		# self.time = time
	
	# def start(self, facility):
		# self.facility = facility
	
	# def tick(self):
		# if self.time:
			# self.time -= 1
		# return self.time
	
	# def __func__(self):
		# self.tick()
	
	
# class Mail(Service):
	# def __init__(self, facility, time=2):
		# self.facility = facility
		# self.time = time

# class Robbery(Service):
	# def __init__(self, facility, time=1):
		# self.facility = facility
		# self.time = time
	
	# def tick(self):
		# facility.queue = []
	
# def mail(self):
	# None
	
def robbery(facility, client):
	facility.timer = 0
	facility.queue = []
	facility.current = None
	facility.loger(client, 'robbery')
	# print("Detta är ett rån!")
