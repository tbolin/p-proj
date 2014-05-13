# -*- coding: UTF-8 -*-

# P-uppgift
# main

from random import randint
from places import *
import services

		
def parse_mail_log(log):
	# Function that defines how a log should be parsed
	things = [[i, conv_time(time), text, person.name, person.errands.get('mail',None), number] for (i, time, text, person, number) in log]
	# 0	id
	# 1	when
 	# 2 what
	# 3 who
	# 4 errands
	# 5	how
	events = {	"next":"{1} \t customer {3} leaves ",
				"start":"and customer {3} with {4} letters is served.\n",
				"done":"{1} \t customer {3} leaves and the queue is empty.\n",
				"add":"{1} \t customer {3} with {4} letters enters ",
				"startn":"and is immediately served. \n",
				"addq":"{1} \t customer {3} enters and is put in queue in place {5}\n",
				"robberyw":"{1} \t {3} enters enters, tries to rob the store, {5} \n",
				"robberyl":"{1} \t {3} enters enters, tries to rob the store, {5} \n",
				"open":"{1} \t {3} Opens the store \n",
				"close":"{1} \t {3} Closes the store \n"
			}
	str = "".join(events.get(post[2], "").format(*post) for post in things)
	if log.customers: 
		misc = [log.customers, log.q_time, (log.q_time/log.customers)*60]
		str += "\nSTATISTICS: {0} customers, queue time {1} minutes = {2:.1f} s/customer".format(*misc)
	return str
	
def gen_errands():
	# Defines which errands a newly generated person 
	# should be given
	errands = 1
	if not randint(0,1000):
		return {'robbery':1}
	flipp = randint(0,1)
	while flipp:
		errands += 1
		flipp = randint(0,1)
	return {'mail':errands}	

def main():
	open = 9
	close = 18
	max_time = close*60
	start_time = open*60
	skrutt = World(start_time, generator = gen_errands)	# This is the world instance
	franco = Person("Franco") # Mrs. Franco
	office = Facility(skrutt, services={'mail','robbery'}, parser=parse_mail_log, staff=franco, state=False) # The office
	skrutt.run(max_time)
if __name__ == '__main__': main()








