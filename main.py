# -*- coding: UTF-8 -*-

# P-uppgift
# main
# Contains classes for representing the world, facilities and people

# TODO
# World, facility, and Person should probably 
# be moved to a sepparate file together with support classes

from random import randint
import services

def conv_time(start, time):
	return "{0:02d}:{1:02d}".format(start+(time//60),time%60)

def gen_errands():
	errands = 1
	if not randint(0,1000):
		return {'robbery':1}
	flipp = randint(0,1)
	while flipp:
		errands += 1
		flipp = randint(0,1)
	return {'mail':errands}

class Person():
	__id = 0
	def __init__(self, errands=[]):
		if not errands: self.errands = gen_errands()
		self.id = Person.__id
		Person.__id += 1
		
	def attach(self, errand, number):
		if callable(errand):
			self.errands[errand.__name__] = number
		
class Log:
	__id = 0
	def __init__(self, world, facility):
		self.id = Log.__id
		Log.__id += 1
		self.world = world
		self.who = []
		self.what = []
		self.when = []
	
	def add(self, person, event):
		self.who.append(person)
		self.what.append(event)
		self.when.append(self.world.time)
	
	def __call__(self, person, event):
		self.add(person, event)
	
	def __iter__(self):
		for (i, (time, text)) in enumerate(zip(self.when, self.what)): 
			yield conv_time(0, time) + "\t" + text
	
	def __repr__(self):
		return "\n".join([s for s in self])
		
		
class Facility():
	def __init__(self, world, queue=[], services=set(), p_time=2):
		self.current = None
		self.process = None
		self.queue = queue
		self.works = []
		self.timer = 0
		self.services = services
		self.p_time = p_time
		self.loger = Log(world, self)
		world.attach(self)
	
	def add_client(self, client):
		if self.services & client.errands.keys(): 
			if self.current: 
				self.loger(client, 'add'+str(len(self.queue)+1))
				self.queue.append(client)
			else: 
				self.queue.append(client)
				self.loger(client, 'add')
	
	def next(self):
		if not self.queue: return False
		client = self.queue.pop(0)
		for k,v in client.errands.items():
			if k in self.services:
				func = getattr(services, k, None)
				if callable(func):
					func(self, client)
					return False
				self.timer += v*self.p_time
		self.loger(client, 'start')
		self.current = client
		return True # True if a new batch was started
		
	def done(self):
		self.loger(self.current, 'done')
		self.current = None
		
	def step(self):
		if not self.timer:
			if self.current:
				self.done()
			if not self.next(): return
		else:
			self.timer -= 1

class World:
	def __init__(self, time=0):
		self.time = time
		self.places = []
		self.people = []
		
	def attach(self, facility):
		self.places.append(facility)
		
	def step(self):
		for f in self.places:
			f.step()
		self.time += 1
		
def main():
	open = 9
	close = 18
	# Open 9-18, 1 minute resolution => 
	max_time = close*60
	time = open*60
	skrutt = World(time)
	office = Facility(skrutt, services={'mail','robbery'})
	
	while skrutt.time <= max_time or office.current:
		if skrutt.time <= max_time and not randint(0, 5): 
			cli = Person()
			office.add_client(cli)
		skrutt.step()
	print(office.loger)
	
	# print("Total wait time:", wait, "minutes")
	# print("Number of customers:", Franco.counter)
	# print("Average wait time:", round(wait/Franco.counter, 2))
if __name__ == '__main__': main()








