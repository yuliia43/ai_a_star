import pdb
import math

class State:
	fullness = []
	next_states = []
	weights = []               #array that contains g(x) to state from `next_states` with the same index
	prev_states = []
	distance_to_final = 0      #h(x)
	fx = 0                     #f(x)

	def __init__(self, fullness):
		self.fullness = fullness
		self.next_states = []
		self.weights = []
		self.prev_states = []
		self.distance_to_final = 0
		self.fx = 0

	def __eq__(self, another):
		return self.fullness == another.fullness

	def __lt__(self, another):
		return self.fx < another.fx


class TreeBuilder:
	capacity = []     #maximal capacity of barrels
	states = []
	first_state = None
	final_state_fullness = []
	closed = []

	def __init__(self, capacities, final_state_fullness, first_state=None):
		self.capacity = capacities
		if first_state == None:
			first_state = State([max(capacities), 0, 0])
		self.first_state = first_state
		self.states.append(first_state)
		self.final_state_fullness = final_state_fullness

	def get_states_tree(self):
		self.set_heuristic(self.first_state)
		self.build_states_tree(self.first_state)


	def build_states_tree(self, state):
		for i in range(len(state.fullness)):     #index of barrel from which water will be poored out
			if (state.fullness[i] != 0):
				for j in range(len(state.fullness)):    #index of barrel to which water will be poored in
					if i != j and state.fullness[j] != self.capacity[j]:
						new_state = State(state.fullness[:])
						dif = min(self.capacity[j]-new_state.fullness[j], state.fullness[i])
						new_state.fullness[i] = new_state.fullness[i]-dif
						new_state.fullness[j] = new_state.fullness[j]+dif
						state_index = self.find_state(new_state)
						if state_index != None:
							new_state = self.states[state_index]
						state.next_states.append(new_state)
						weight_value = 1
						state.weights.append(weight_value)
						new_state.prev_states.append(state)
						if state_index == None:
							self.set_heuristic(new_state)
							self.states.append(new_state)
							self.build_states_tree(new_state)


	def set_heuristic(self, state):                              #sets h(x)
		distance_to_final = 0
		if state.fullness[0] == self.final_state_fullness[0]:
			state.distance_to_final = 0
			return
		if state.fullness[0] == 0:
			state.distance_to_final = self.capacity[0]
			return
		for i in range(len(state.fullness)):
			fullness_of_i_barrel = self.capacity[i]
			if state.fullness[0] == fullness_of_i_barrel:
				state.distance_to_final = fullness_of_i_barrel
				return
		#if cyckle ended and function has not been ended
		max_value = 0
		for i in range(1,len(state.fullness)):
			rest = state.fullness[0]%self.capacity[i]
			if rest > max_value:
				max_value = rest
		state.distance_to_final = max_value

	def a_star_algorithm(self):                         #realization of algorithm
		open_queue = []
		self.first_state.fx = self.first_state.distance_to_final
		state = self.first_state
		self.closed.append(state)
		while state.fullness != self.final_state_fullness:
			states_queue = state.next_states[:]
			for i in range(len(states_queue)):
				states_queue[i].fx = state.weights[i]+states_queue[i].distance_to_final
			states_queue.sort()
			for state_in_queue in states_queue:
				if self.in_closed_list(state_in_queue):
					states_queue.remove(state_in_queue)
			if states_queue[0].fx <= state.fx:                    
				state = states_queue[0]
				open_queue = states_queue[1:]+open_queue
			else:   #if state's f(x) is bigger than previous state's, we break this search
				state = open_queue[0]
				open_queue.pop(0)
			self.closed.append(state)			


	def in_closed_list(self, state):
		try:
			self.closed.index(state)
			return True
		except:
			return False


	def get_result_string(self):
		result_string = ''
		for barrel_capacity in self.capacity:
			result_string = result_string + '|'+ '{:^15}'.format(str(barrel_capacity) + "l barrel")
		result_string = result_string + '|\n' + '_'*49 + '\n'
		for state in self.closed:
			for value in state.fullness:
				result_string = result_string + '|'+ '{:^15}'.format(value)
			result_string = result_string + '|\n'
		return result_string


	def find_state(self, state):      #returns index of state in list, or None if state not founded
		try:
			return self.states.index(state)
		except:
			return None

#builder = TreeBuilder([10,3,4], [5,1,4])
builder = TreeBuilder([12,5,7], [6,0,6])
builder.get_states_tree()
builder.a_star_algorithm()
print builder.get_result_string()