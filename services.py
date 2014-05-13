# -*- coding: UTF-8 -*-

# P-uppgift
# errands

# Contains functions representing 
# services a facility can provide

import random

def robbed(facility):
	if facility.attraction < 5:    facility.attraction += 0.5
	elif facility.attraction > 8: facility.attraction -= 3
	elif facility.attraction > 5: facility.attraction -= 1
	else: facility.effects = []
	
def robbery(facility, client, state):
	if state == 'add':
		facility.timer = 0
		facility.queue = []
		facility.current = None
		if not random.randint(0,4):
			facility.loger(client, 'robberyl', "and manages to overpower Franco")
			facility.attraction = 20
		else:
			facility.loger(client, 'robberyw', 'but is quickly tickled into submision by Franco')
			facility.attraction = 2
		facility.effects.append(robbed)
		return False
