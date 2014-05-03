# -*- coding: UTF-8 -*-

# P-uppgift
# QnD-main

from random import randint

def conv_time(start, time):
	return "{0:02d}:{1:02d}".format(start+(time//60),time%60)

def gen_errands():
	errands = 1
	flipp = randint(0,1)
	while flipp:
		errands += 1
		flipp = randint(0,1)
	return {'post':errands}

class Person():
	__id = 0
	def __init__(self, errands=0):
		if not errands: self.errands = gen_errands()
		self.id = Person.__id
		Person.__id += 1

class Log:
	__id = 0
	def __init__(self, world, parrent):
		self.id = Event.__id
		Logg.__id s+= 1
		self.who = []
		self.what = []
		self.when = []
	
	def add(self, person, event):
		self.who.append(person)
		self.what.append(event)
		self.when.append(self.world.time())
	
	def __iter__(self):
		for i, time, text in enumerate(zip(when, what)): 
			yield conv_time(time, 9) + "\t" + text
	
	def __repr__(self):
		for p in self: print(p)
		
		
class facility():
	def __init__(self, world, queue=[], service='post', p_time=2):
		self.current = None
		self.bussy = 0
		self.log_counter = 0
		self.queue = queue
		self.service = service
		self.p_time = p_time
		self.wait_time = 0
		self.loger = Log(world, self)
		self.done = []
	
	def add_client(self, client):
		if self.service in client.errands: 
			if self.current: self.loger(client, 'add'+len(queue)+1)
			else: 
			self.queue.append(client)
	
	def log(self, person, event):
		self.logger.add(person,event)
	
	def step(self):
		# Step forward and return True if ready for next task
		if self.current and not self.current.errand[self.service]:
			self.log(self.current, 'done')
			self.done.append(self.current)
			self.counter += 1
			self.current = None
		elif self.current:
			self.current.errand[self.service] -= 1
		if self.queue and self.current is None
			self.current = self.queue.pop(0)
			self.log(self.current, 'next')
		self.wait_time += len(self.queue)
		return False

class World:
	def __init__(self):
		self.time = 0
		self.places = []
		self.people = []
		
	def step(self):
		for f in places:
			f.step()
		self.tie += 1
		
def main():
	open = 9
	close = 18
	# Open 9-18, 1 minute resolution => 
	max_time = (close-open)*60
	print(max_time)
	time = 0
	Franco = facility()
	queue = []
	log = []
	wait = 0
	while time <= max_time or Franco.bussy:
		if not randint(0,5) and time <= max_time:
			queue.append(Person())
			log.append(conv_time(open,time)+" Customer "+str(queue[-1].id)+" enters")
			if not Franco.bussy:
				log[-1] += " and is immediately served."
			else: 
				log[-1] += " and is put in queue as #"+str(len(queue))+"."
		if queue and not Franco.bussy:
			Franco.start_process(queue.pop(0))
		done = Franco.step()
		if done and queue:
			log.append(conv_time(open, time)+" customer " + str(done.id) + " leaves, and cusomer "+
			str(queue[0].id)+ " is served.")
		elif done:
			log.append(conv_time(open, time)+" customer " + str(done.id) + " leaves, queue is empty")
		wait += len(queue)
		time +=1
	for l in log:
		print(l)
	print("Total wait time:", wait, "minutes")
	print("Number of customers:", Franco.counter)
	print("Average wait time:", round(wait/Franco.counter, 2))
if __name__ == '__main__': main()








