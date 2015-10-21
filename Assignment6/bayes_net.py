# YOU THERE!! STOP CHEATING OFF OF THIS! #

##########################################
#	Bayes Net Disease Predictor	 #
#	     Brennan McConnell		 #
##########################################

NO_REASONING = 0
SIBLING = 3
PR = 1
DR = 2

class Node(object):

	def __init__(self, name, cpn):
		self.name = name
		self.probs = {}
		self.parents = {}
		self.marginal_prob_calculated = False
		self.marginal_probability_name = cpn
		self.marginal_probability = None

	def add_probability(self, key, value):
		self.probs[key] = value

	def add_parent(self, node):
		self.parents[node.name] = node


class Bayesian_Network(object):

	def __init__(self):
		self.nodes = {}

	def add_node(self, node):
		self.nodes[node.name] = node

	def calculate_marginal_probabilities(self):
		for RV in self.nodes.values():
			if RV.marginal_prob_calculated == False:
				self.solve_marginal_prob(RV)

	def solve_marginal_prob(self, RV):
		if (len(RV.parents) == 0):
			results = RV.probs.values()
			if (len(results) != 1):
				print "ERROR FOUND!"
			else:
				RV.marginal_probability = results[0]
				RV.marginal_prob_calculated = True
		else:
			RV_marg_prob = 0.0
			rvp_marg_probs = {}
			for rvp in RV.parents.values():
				if (rvp.marginal_prob_calculated == False):
					self.solve_marginal_prob(rvp)
				rvp_marg_probs[rvp.marginal_probability_name] = rvp.marginal_probability

			for (key, val) in RV.probs.items():
				cur = 1.0
				negate = False
				for char in key:
					if (char == '~'):
						negate = True
					else:
						if (negate == False):
							cur *= rvp_marg_probs[char]
						else:
							negate = False
							cur *= (1 - rvp_marg_probs[char])
				RV_marg_prob += val * cur

			RV.marginal_probability = RV_marg_prob
			RV.marginal_prob_calculated = True


	def solve_conditional_probability(self, RV1, RV2, r1status, r2status):
		# Solve P(RV1 | RV2)
		reasoning = self.decide_direction_of_reasoning(RV1, RV2)
		if (reasoning == PR): # freebie pretty much, given in initial data
			
			if (RV1.probs.has_key(RV2.marginal_probability_name)):
				if r1status == "~":
					return 1-RV1.probs[r2status + RV2.marginal_probability_name]
				else:
					return RV1.probs[r2status + RV2.marginal_probability_name]


			else: # We need to sum something out

				if not (RV1.parents.has_key(RV2.name)): # we are two nodes below the parent
					rvp = None
					for parent in RV1.parents.values():
						rvp = parent
					x = self.solve_conditional_probability(RV1, rvp, r1status, "")
					r1 = self.solve_conditional_probability(rvp, RV2, "", r2status)
					y = self.solve_conditional_probability(RV1, rvp, r1status, "~")
					r2 = 1-r1

					return (x*r1) + (y*r2)

				else: # We are 1 node below the parent
					# Sum out RV1's parents
					rvp_prob_to_sum_out = None
					rvp_marg_conditioning_on = RV2.name

					for rvp in RV1.parents.values():
						if (rvp.name != RV2.name):
							rvp_prob_to_sum_out = (rvp.marginal_probability_name, rvp.marginal_probability)
					
					x = ((r2status+RV2.marginal_probability_name+rvp_prob_to_sum_out[0], rvp_prob_to_sum_out[0]+r2status+RV2.marginal_probability_name), RV2.marginal_probability * rvp_prob_to_sum_out[1])
					y = ((r2status+RV2.marginal_probability_name+"~"+rvp_prob_to_sum_out[0], "~"+rvp_prob_to_sum_out[0]+r2status+RV2.marginal_probability_name), RV2.marginal_probability * (1-rvp_prob_to_sum_out[1]))


					r1 = x[1] * RV1.probs.get(x[0][0], RV1.probs.get(x[0][1], False))
					r2 = y[1] * RV1.probs.get(y[0][0], RV1.probs.get(y[0][1], False))

					if r1status == "~":
						return 1 - ((r1 + r2) / RV2.marginal_probability)
					else:
						return (r1 + r2) / RV2.marginal_probability
			
		elif (reasoning == DR):
			# We can use Predictive reasoning to work backwards
			# i.e. P(A|B) = P(B|A)P(A)/P(B)
			x = self.solve_conditional_probability(RV2, RV1, r2status, "")
			x *= RV1.marginal_probability
			x /= RV2.marginal_probability

			if (r1status == "~"):
				return (1-x)
			else:
				return x

		elif (reasoning == NO_REASONING):
			return 1

		elif (reasoning == SIBLING):
			shared_parent = False
			RV3 = None
			for rvp1 in RV1.parents.values():
				for rvp2 in RV2.parents.values():
					if rvp1 == rvp2:
						RV3 = rvp1
						shared_parent = True
						break
			if (shared_parent): # There is intercausal probability affects
				# These two effects depend on each other through there conditional dependence on the parent
			
				x = self.solve_conditional_probability(RV1, RV3, r1status, "")
				r1 = self.solve_conditional_probability(RV3, RV2, "", r2status)
				y = self.solve_conditional_probability(RV1, RV3, r1status, "~")
				r2 = self.solve_conditional_probability(RV3, RV2, "~", r2status)

				return (x*r1) + (y*r2)

			else:
				return RV1.marginal_probability


	def decide_direction_of_reasoning(self, RV1, RV2):
		if (RV1.name == RV2.name):
			return NO_REASONING

		queue = []
		# If RV2 is above RV1, this is Predictive Reasoning
		queue.append(RV1)
		while (len(queue) > 0):
			for result in queue:
				if (result.name == RV2.name):
					# "Predictive Reasoning"
					return PR
				queue.remove(result)
				for item in result.parents.values():
					queue.append(item)


		queue = []
		queue.append(RV2)
		# If RV1 is above RV2, this is Diagnostic Reasoning
		while (len(queue) > 0):
			for result in queue:
				if (result.name == RV1.name):
					# "Diagnostic Reasoning"
					return DR
				queue.remove(result)
				for item in result.parents.values():
					queue.append(item)


		return SIBLING


	def solve_joint_probabilities(self):
		return None



def construct_bayes_net():
	P = Node("Pollution", "P")
	P.add_probability("P", 0.9)
	S = Node("Smoker", "S")
	S.add_probability("S", 0.3)
	C = Node("Cancer", "C")
	C.add_probability("~PS", 0.05)
	C.add_probability("~P~S", 0.02)
	C.add_probability("PS", 0.03)
	C.add_probability("P~S", 0.001)
	X = Node("XRay", "X")
	X.add_probability("C", 0.9)
	X.add_probability("~C", 0.2)
	D = Node("Dyspnoea", "D")
	D.add_probability("C", 0.65)
	D.add_probability("~C", 0.3)

	C.add_parent(P)
	C.add_parent(S)
	X.add_parent(C)
	D.add_parent(C)

	BN = Bayesian_Network()
	BN.add_node(P)
	BN.add_node(S)
	BN.add_node(C)
	BN.add_node(X)
	BN.add_node(D)
	BN.calculate_marginal_probabilities()

	print BN.solve_conditional_probability(X, D, "", "")


	return BN


if __name__ == "__main__":
	bayes_net = construct_bayes_net()
#	for node in bayes_net.nodes.values():
#		print node.marginal_probability_name, ":", round(node.marginal_probability, 4)









