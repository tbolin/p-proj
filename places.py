# -*- coding: UTF-8 -*-

# P-uppgift
# Classes representing the world, facilities and people

from random import randint
import services

def default_generator():
	# used as a default for setting peoples errands
		return {}

class World:
	def __init__(self, time=0, population=0, generator=default_generator):
		self.time = time
		self.places = []
		self.population = population
		self.generator = generator
		if not population: self.people = []
		else: self.people = [Person(errands = generator()) for i in range(population)]
		
	def attach(self, facility):
		self.places.append(facility)
		
	def step(self):
		for f in self.places:
			# check if any customers should be added
			if f.state and not randint(0, int(f.attraction)):
				if self.population: cli = self.people.pop(randint(1,len(self.people)))
				else: cli = Person(errands=self.generator())
				f.add_client(cli)
			f.step()
		self.time += 1
	
	def is_open(self):
		# check if any facilities is still doing bussnies
		for p in self.places:
			if p.state or p.current:
				return True
		return False
	
	def done(self):
		for f in self.places:
			print(f.loger.parsed())
	
	def run(self, stop, hard_stop=-1):
		if hard_stop <= self.time: hard_stop = float('inf') # default: run until last facility closes 
		while (self.time <= stop or self.is_open()) and self.time <= hard_stop:
			self.step()
		self.done()

class Facility():
	def __init__(self, world, queue=[], services=set(), parser=None, p_time=2, attraction=5, open=9, close=18, staff=None, state=True):
		self.world = world
		self.current = None
		self.process = None
		self.queue = queue
		self.works = []
		self.timer = 0
		self.services = services
		self.p_time = p_time
		self.attraction = attraction
		self.open = open*60
		self.close = close*60
		self.staff = staff
		self.state = state # True if accepting new cutomers
		self.loger = Log(world, self, parser, customers=0, q_time=0)
		self.effects = []
		world.attach(self)
	
	def add_client(self, client):
		if self.services & client.errands.keys(): 
			# check for robbery
			for k,v in client.errands.items():
				if k in self.services:
					func = getattr(services, k, None)
					if callable(func):
						cont = func(self, client, "add")
						if not cont: return
			if self.current: 
				self.loger(client, 'addq', len(self.queue)+1)
				self.queue.append(client)
			else: 
				self.queue.append(client)
				self.loger(client, 'add')
	
	def next(self):
		if not self.queue: return False # False if queue is empty
		client = self.queue.pop(0)
		for k,v in client.errands.items():
			if k in self.services:
				func = getattr(services, k, None)
				if callable(func):
					func(self, client, 'next')
					return False # or the errand has a custom function
				self.timer = v*self.p_time-1
		if self.loger.what[-1] == 'next':
			self.loger(client, 'start')
		else: 
			self.loger(client, 'startn')
		self.current = client
		return True # True if a new batch was started
		
	def done(self):
		if self.queue:
			self.loger(self.current, 'next')
		else:
			self.loger(self.current, 'done')
		self.loger.customers += 1
		self.world.people.append(self.current)
		self.current = None
		
	def step(self):
		# Check if the store should open/close
		if self.state and (self.world.time%(60*24) <= self.open or self.close <= self.world.time%(60*24)):
			self.state = False
			self.loger(self.staff, "close")
		elif not self.state and self.world.time%(60*24) > self.open and self.close > self.world.time%(60*24):
			self.state = True
			self.loger(self.staff, "open")
		# apply any effects to the facility
		for effect in self.effects:
			effect(self)
		# Check if default task is running
		if not self.timer:
			if self.current:
				self.done()
			self.next()
		else:
			self.timer -= 1
		self.loger.q_time += len(self.queue)
	
class Person():
	__id = 0
	def __init__(self, name=None, errands={}):
		self.errands = errands
		self.id = Person.__id
		if name: self.name = name
		else: self.name = self.id
		Person.__id += 1
		
	def attach(self, errand, number):
		if callable(errand):
			self.errands[errand.__name__] = number
		
class Log:
	__id = 0
	def __init__(self, world, facility, parser=None, **kwargs):
		self.id = Log.__id
		Log.__id += 1
		self.world = world
		self.who = []
		self.what = []
		self.when = []
		self.how = []
		self.parser = parser
		for name, value in kwargs.items():
			setattr(self, name, value)
	
	def add(self, person, event, how=None):
		self.who.append(person)
		self.what.append(event)
		self.when.append(self.world.time)
		self.how.append(how)
	
	def parsed(self):
		if self.parser:
			return self.parser(self)
		else:
			return self.__repr__()
	
	def __call__(self, person, event, how=None):
		self.add(person, event, how)
	
	def __iter__(self):
		for (i, (time, text, person, number)) in enumerate(zip(self.when, self.what, self.who, self.how)): 
			yield (i, time, text, person, number)
	
	def __repr__(self):
		things = ["{0}:\t{1}\t{2}\t{3}\t{4}".format(i, conv_time(time), text, person.name, number) for (i, time, text, person, number) in self]
		return "\n".join(things)

def conv_time(time, start=0):
	"""Converts time in minutes """
	return "{0:02d}:{1:02d}".format(start+(time//60),time%60)