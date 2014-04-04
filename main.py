# -*- coding: UTF-8 -*-

# P-uppgift
# QnD-main

from random import randint

def conv_time(start, time):
	return "{0:02d}:{1:02d}".format(start+(time//60),time%60)

def new_customer():
	errands = 1
	flipp = randint(0,1)
	while flipp:
		errands += 1
		flipp = randint(0,1)
	return errands

class Person():
	__id = 1
	def __init__(self, errands=0):
		if not errands: self.errands = new_customer()
		self.id = Person.__id
		Person.__id += 1
	
class facility():
	def __init__(self):
		self.current = None
		self.bussy = 0
		self.eff = 2
		self.counter = 0
	
	def start_process(self, process):
		if self.bussy: return False
		self.current = process
		self.bussy = self.eff * process.errands +1
		
	def step(self):
		# Step forward and return True if ready for next task
		if not self.bussy: return False
		self.bussy -= 1
		if not self.bussy: 
			process = self.current
			self.current = None
			self.counter += 1
			return process
		return False
		
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








