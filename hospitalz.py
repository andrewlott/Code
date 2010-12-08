#cluster by centroid
#WEIGH by imperativeness
#consider minimizing max-distances between hospitals
#maybe use clusters from old code
#import Queue
import math
import random
#from scipy.cluster.vq import whiten,kmeans2
from numpy import array,zeros
import time

class Ambulance:
	
	def __init__(self,h_x,h_y, id):
		self.x = h_x
		self.y = h_y
		self.q = []
		self.target = []#Person(-1,50,50,float('inf'))
		self.status = -1			# -1 is ready for next, 0 is on way, 1 is full
		self.n_h = tuple([h_x,h_y])	#nearest hospital
		self.id = id

class Person:

	def __init__(self,i,p_x,p_y,t):
		self.i = i
		self.x = p_x
		self.y = p_y
		self.t = t
		
class Hospital:
		
	def __init__(self, h_x, h_y, n_a, id):
		self.x = h_x
		self.y = h_y
		self.n_a = n_a
		self.id = id
	
#q = Queue.PriorityQueue()	
a_lim = 4
ind = 0

ambulances = []

#grid = [[float('inf') for i in range(101)] for j in range(101)]
grid = zeros((101,101))

hospitals = []
people = []

saved = []
died = []

def euclidian(hx,hy,px,py):
	return math.sqrt((px-hx)*(px-hx)+(py-hy)*(py-hy))

	
def k_cluster():
	for i in range(len(hospitals)):
		rand_p = people[random.randrange(0,len(people))]
		hospitals[i].x = rand_p.x
		hospitals[i].y = rand_p.y
	
	best_dist = h_dist()
	for i in range(10):
		for person in people:
			best = 0
			b_d = float('inf')
			#find closest hospital
			for h in hospitals:
				if distance(person.x,person.y,h.x,h.y) < b_d:
					best = hospitals.index(h)
					b_d = distance(person.x,person.y,h.x,h.y)
			b_h = hospitals.pop(best)
			hospitals.append(Hospital(person.x,person.y,b_h.n_a,b_h.id))
			h_d = h_dist()
			if best_dist > h_d:
				best_dist = h_d
			else:
				hospitals.remove(hospitals[len(hospitals)-1])
				hospitals.append(b_h)
	#print best_dist
	return best_dist
	
		
def h_dist():
	total = 0
	for i in range(len(people)):
		total += min(distance(people[i].x,people[i].y,hospitals[0].x,hospitals[0].y),
					distance(people[i].x,people[i].y,hospitals[1].x,hospitals[1].y),
					distance(people[i].x,people[i].y,hospitals[2].x,hospitals[2].y),
					distance(people[i].x,people[i].y,hospitals[3].x,hospitals[3].y),
					distance(people[i].x,people[i].y,hospitals[4].x,hospitals[4].y))
	return total
	
def nearest_h(thing):
	b_h = 0
	best = float('inf')
	for h in hospitals:
		d = distance(thing.x,thing.y,h.x,h.y)
		if d < best:
			best = d
			b_h = h
	return b_h

def nearest_a(thing,time):
	b_a = 0
	best = float('inf')
	for a in ambulances:
		if (len(a.q) < 4) and can_survive(a,thing,time) and a.status == -1:
			d = distance(thing.x,thing.y,a.x,a.y)
			if d < best:
				best = d
				b_a = a
	return b_a
	
def nearest_p(a,time):
	b_p = 0
	best = float('inf')
	for p in people:
		if can_survive(a,p,time):
			d = distance(p.x,p.y,a.x,a.y)
			if d < best:
				best = d
				b_p = p
	return b_p
	
def can_survive(a,person,time):
	for victim in a.q:
		if victim.t - time >= distance(nearest_h(person).x,nearest_h(person).y,person.x,person.y) + distance(person.x,person.y,a.x,a.y):
			return False
	return True
	
def goBack(a,time):
	if len(a.q) == 0:
		return False
	for i in range(len(a.q)):
		if a.q[i].t - time == distance(nearest_h(a).x,nearest_h(a).y,a.x,a.y):
			return True
	return False
	
def d_p(person):
	return (distance(person.x,person.y,ambulances[ind].x,ambulances[ind].y))
	
#maybe make function to sort better, could just be time + distance, or root(distance)

targ = 0
div = 1

def s_func(person):
	return distance(targ.x,targ.y,person.x,person.y)+(person.t/div)
	

def go():
	global people
	global ind
	global targ
	#print len(people)
	for h in hospitals:
		for person in people:
			if person.x == h.x and person.y == h.y:
				saved.append(people.pop(people.index(person)))
				break
	#print len(people)
	for time in range(people[len(people)-1].t+2):
		#print time, ":", ambulances[0].x, ambulances[0].y, ":",ambulances[0].target.i
		for a in ambulances:
			if len(a.q) == 4:
				a.status = 1
				a.target = nearest_h(a)
				
			if a.status == -1:
				#ready to pickup
				

				for i in range(10):
					targ = a
					div = 1
					people = sorted(people, key = s_func)
					p = people[i]
					for j in range(1,10):
						targ = p
						div = 2
						people = sorted(people, key = s_func)
						pp = people[j]
						for k in range(1,10):
							targ = pp
							div = 3
							people = sorted(people, key = s_func)
							ppp = people[k]
							for l in range(1,10):
								targ = ppp
								div = 4
								people = sorted(people, key = s_func)
								pppp = people[l]
								d = distance(p.x,p.y,a.x,a.y) + distance(p.x,p.y,pp.x,pp.y) + distance(pp.x,pp.y,ppp.x,ppp.y) + distance(ppp.x,ppp.y,pppp.x,pppp.y) + distance(pppp.x,pppp.y,nearest_h(pppp).x,nearest_h(pppp).y)
								#print p.x,p.y, "|",pp.x,pp.y, "|",ppp.x,ppp.y, "|",pppp.x,pppp.y, " || ",min(p.t,pp.t,ppp.t,pppp.t), "//", d
								if p != pp and p != ppp and p != pppp and pp != ppp and pp != pppp and ppp != pppp and d+4 < min(p.t,pp.t,ppp.t,pppp.t) - time:
									a.target = [p,pp,ppp,pppp]
									break
								#print ""
							if len(a.target) == 4:
								break
						if len(a.target) == 4:
							break
					if len(a.target) == 4:
						break
				for guy in a.target:
					people.remove(guy)
				#print "Target",a.id,":",len(a.target)
				#print a.target

				''' THIS GOES WITH THE OTHER CHUNK THAT NEEDS BREAKS
				for p in people:
					if nearest_a(p,time) == a:	#watch out for the ones at the same location!!!
						a.target = [people.pop(people.index(p))]	#how do I want to follow targets? target = array of them?
						break
				clust_score = float('inf')
				cluster = 0
				c = 0
				'''
				
				'''
				targ = a.target[0]
				people = sorted(people, key = lambda person: s_func)
				print time, ":",len(people)
				a.target.append(people.pop(0))
				a.target.append(people.pop(0))
				a.target.append(people.pop(0))
				'''
				
				'''
				for p in people:
					for pp in people:
						d = distance(p.x,p.y,a.x,a.y) + distance(p.x,p.y,pp.x,pp.y)
						c += 1
						print c
						if p != pp and d + 4 < p.t and d + 4 < pp.t:
							for ppp in people:
								if pp != ppp and ppp != p:
									d = distance(p.x,p.y,a.x,a.y) + distance(p.x,p.y,pp.x,pp.y) + distance(pp.x,pp.y,ppp.x,ppp.y) + distance(ppp.x,ppp.y,nearest_h(ppp).x,nearest_h(ppp).y)
									if clust_score > d and d+4 < -time + p.t and d+4 < -time + pp.t and d+4 < -time + ppp.t and d+4 < -time + a.target[0].t:
										clust_score = d
										cluster = [p,pp,ppp]
										for guys in cluster:
											people.remove(guys)
										a.target.extend(cluster)
										break
							#add all those breaks
										
				'''
				if len(a.target) == 4:
					a.status = 0
				else:
					a.status = -2
				
			if a.status == 0:
				#go to target
				if a.x != a.target[0].x:
					a.x += (a.target[0].x-a.x)//(abs(a.target[0].x-a.x))
				elif a.y != a.target[0].y:
					a.y += (a.target[0].y-a.y)//(abs(a.target[0].y-a.y))
				else:
					#found
					print "Ambulance " + str(a.id) + " " + str(a.target[0].i) + " (" + str(a.target[0].x) + "," + str(a.target[0].y) + "," + str(a.target[0].t) + ")"
					a.q.append(a.target.pop(0))
					a.status = 2
			elif a.status == 1:
				#full, return to hospital
				if a.x != a.target.x:
					a.x += (a.target.x-a.x)//(abs(a.target.x-a.x))
				elif a.y != a.target.y:
					a.y += (a.target.y-a.y)//(abs(a.target.y-a.y))
				else:
					a.status = 3
					#maybe make this better
					while len(a.q) > 0:	
						#print a.id,"Drop",a.q[len(a.q)-1].i
						saved.append(a.q.pop(len(a.q)-1))
					print "Ambulance " + str(a.id) + " (" + str(a.target.x) + "," + str(a.target.y) + ")"
					a.target = []
			elif a.status == 2:
				#kill that extra minute for pick-up
				a.status = 0
			elif a.status == 3:
				#drop off, meng
				a.status = -1
				
								
			'''
			ind = ind%len(ambulances)
			if len(a.q) == 4:
				a.status = 1
			if a.status == -1:
				#ready to pick-up
				people = sorted(people,key=d_p)
				for person in people:
					if nearest_a(person,time) == a:
						print "Target",people[people.index(person)].i
						a.target = people.pop(people.index(person))
						a.status = 0
						break
				if a.status == -1:
					a.target = people.pop(0)
					a.status = 0
			if a.status == 0:
				#on way to target
				if a.x != a.target.x:
					a.x += (a.target.x-a.x)//(abs(a.target.x-a.x))
				elif a.y != a.target.y:
					a.y += (a.target.y-a.y)//(abs(a.target.y-a.y))
				else:
					a.status = 5
					print "Pickup",a.target.i
					a.q.append(a.target)
			elif a.status == 1:
				#return to hospital
				a.target = nearest_h(a)
				
				if a.x != a.target.x:
					a.x += (a.target.x-a.x)//(abs(a.target.x-a.x))
				elif a.y != a.target.y:
					a.y += (a.target.y-a.y)//(abs(a.target.y-a.y))
				else:
					a.status = 5
					while len(a.q) > 0:	
						print "Drop",a.q[len(a.q)-1].i
						saved.append(a.q.pop(len(a.q)-1))
			else:
				#print "Pickup"
				#picking up atm or dropping at hospital
				a.status = -1
			'''
		#death
		p = 0
		while p < len(people):
			if time > people[p].t:
				died.append(people.pop(p))
				p -= 1
			p += 1
		#graph(time)
		#print time
		
				
#+1 minute to drop off 4 people
#+1 minute to pick up
	
def distance(xp, yp, xa, ya):
	return abs(xp-xa) + abs(yp-ya)
	
def graph(time):
	s = ''
	for row in range(101):
		for col in range(101):
			found = False
			for h in hospitals:
				if row == h.x and col == h.y:
					s += 'H'
					found = True
				else:
					for a in ambulances:
						if row == a.x and col == a.y and not found:
							s += 'A'
							found = True
							break
							
					for person in people:
						if not found and row == person.x and col == person.y:
							s += 'P'
							found = True
							break
			if not found:
				s += '.'
		s += '\n'
	print s
	print time
	if time > 70:
		t.sleep(1)
	
if __name__ == "__main__":
	#try:
	#	s = input('File name: ')
	#except:
	s = 'ambu2010_2.txt'
	f = open(s)
	f.readline()#kill first line
	
	max_x = 0
	max_y = 0
	status = 0
	p_num = 0
	t = time.time()
	for line in f:
		#print line
		if str.isdigit(line[0]):
			if status == 0:
				temp = line.strip().split(',')
				#max_x = max(max_x,int(temp[0]))
				#max_y = max(max_y,int(temp[1]))
				#q.put(tuple([int(temp[2]),int(temp[0]),int(temp[1])]))
				people.append(Person(int(p_num),int(temp[0]),int(temp[1]),int(temp[2])))
				#grid[int(temp[0])][int(temp[1])] = int(temp[2])
				p_num += 1
			else:
				hospitals.append(Hospital(0,0,int(line.strip()),status-1))
				status += 1
				
		else:
			status = 1
		
	people = sorted(people, key = lambda person: person.t)

	
	#people.reverse()
	b = k_cluster()
	b_h = list(hospitals)
	for i in range(0):
		temp = k_cluster()
		if temp > b:
			b = temp
			b_h = list(hospitals)
	
	
	hospitals = b_h
	hospitals = sorted(hospitals, key = lambda h: h.id)
	#print "\n\n"
	id = 0
	for h in hospitals:
		for i in range(h.n_a):
			ambulances.append(Ambulance(h.x,h.y,id))
			id+=1
			#print ambulances[len(ambulances)-1].id, ":",ambulances[len(ambulances)-1].x,ambulances[len(ambulances)-1].y
	#print time.time()-t
	s = "Hospitals "
	for i in range(len(hospitals)):
		s += str(hospitals[i].id) + " (" + str(hospitals[i].x) + "," + str(hospitals[i].y) + ") "
	print s
	go()
	
	#print "Dead:",len(died)
	#print "Saved:",len(saved)
	#print "Left:",len(people)
	#print time.time()-t

