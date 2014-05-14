# -*- coding: UTF-8 -*-

# P-uppgift grupdat VT-2014
# Tobias Bolin
# errands

# Contains functions representing 
# services a facility can provide

import random

def robbed(facility):
	if facility.attraction < 4:    facility.attraction += 0.5
	elif facility.attraction > 8: facility.attraction -= 3
	elif facility.attraction > 4: facility.attraction -= 1
	else: facility.effects = []
	
def robbery(facility, client, state):
	if state == 'add':
		facility.timer = 0
		facility.queue = []
		facility.current = None
		# Franco wins 4 out of 5
		if not random.randint(0,4):
			facility.loger(client, 'robberyl', "and manages to overpower Franco")
			facility.attraction = 20
		else:
			facility.loger(client, 'robberyw', 'but is quickly tickled into submision by Franco')
			facility.attraction = 1
		facility.effects.append(robbed)
		return False
