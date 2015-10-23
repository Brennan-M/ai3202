# YOU THERE!! STOP CHEATING OFF OF THIS! #
# JK, this is unreadable code, good luck #

##########################################
#	Bayes Net Disease Predictor	 #
#	     Brennan McConnell		 #
##########################################

import getopt, sys

NO_REASONING = 0
SIBLING = 3
PR = 1
DR = 2
INT_CAUS = 4
COMBINED = 5
NEITHER = 6
INHERENTLY_GIVEN = 7


class Node(object):


	def __init__(self, name, cpn):
		self.name = name
		self.probs = {}
		self.parents = {}
		self.children = {}
		self.marginal_prob_calculated = False
		self.marginal_probability_name = cpn
		self.marginal_probability = None


	def add_probability(self, key, value):
		self.probs[key] = value


	def add_parent(self, node):
		self.parents[node.name] = node


	def add_child(self, node):
		self.children[node.name] = node


	def change_probability(self, key, value):
		self.probs[key] = value


class Bayesian_Network(object):


	def __init__(self):
		self.nodes = {}


	def add_node(self, node):
		self.nodes[node.name] = node


	def update_probability(self, arg, newValue):
		node = None

		if (arg == "P"):
			node = self.nodes["Pollution"]

		elif (arg == "S"):
			node = self.nodes["Smoker"]
		
		node.change_probability(arg, newValue)

		for n in self.nodes.values():
			n.marginal_prob_calculated = False
		
		self.calculate_marginal_probabilities()


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
		if (reasoning == PR): 
			if (RV1.probs.has_key(RV2.marginal_probability_name)): # freebie pretty much, given in initial data
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
			
			y = RV2.marginal_probability

			if (r2status == "~"):
				y = 1-y
			x /= y

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
				if (r1status == "~"):
					return 1 - RV1.marginal_probability
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


	def solve_joint_probability_pair(self, RV1, RV2, r1status, r2status):
		# This returns correctly regardless of dependence between RV1 and RV2
		if r2status == "~":
			mp = 1 - RV2.marginal_probability
		else:
			mp = RV2.marginal_probability

		return mp * self.solve_conditional_probability(RV1, RV2, r1status, r2status)


	def solve_conditional_on_joint_probability(self, RV1, RV2, RV3, r1s, r2s, r3s): #Signifies multiple evidence
		RV_arr = [RV1, RV2, RV3]
		RV_status_arr = [r1s, r2s, r3s]

		# Can we just solve it given initial data (i.e. P(c|s,p) )
		if (RV1.probs.has_key(r2s+RV2.marginal_probability_name+r3s+RV3.marginal_probability_name) or RV1.probs.has_key(r3s+RV3.marginal_probability_name+r2s+RV2.marginal_probability_name)): # freebie pretty much, given in initial data
			x = RV1.probs.get(r2s+RV2.marginal_probability_name+r3s+RV3.marginal_probability_name, RV1.probs.get(r3s+RV3.marginal_probability_name+r2s+RV2.marginal_probability_name, False))
			if (r1s == "~"):
				return 1 - x
			return x
			
		#find which variable the other two depend on
		reasoning = self.determine_reasoning_with_mult_evidence(RV1, RV2, RV3)

		if (reasoning[0] == INHERENTLY_GIVEN):
			if (r1s == RV_status_arr[reasoning[1]-1]):
				return 1.0
			return 0.0

		if reasoning[0] == INT_CAUS:

			RV_root = reasoning[1]

			# CASE 1
			# If RV1 (P) is conditionally independent from evidence E given evidence Root
			# Then we don't care about evidence E
			# ex. P (x | c,s) = P (x|c) or P (s |c,x) = P (s|c)

			if (RV_root == RV2):
				if (RV2.parents.has_key(RV3.name) and RV2.children.has_key(RV1.name)):
					return self.solve_conditional_probability(RV1, RV2, r1s, r2s)
				if (RV2.parents.has_key(RV3.name) and RV3.parents.has_key(RV1.name)):
					return self.solve_conditional_probability(RV1, RV3, r1s, r3s)
			elif (RV_root == RV3):
				if (RV3.parents.has_key(RV2.name) and RV3.children.has_key(RV1.name)):
					return self.solve_conditional_probability(RV1, RV3, r1s, r3s)
				if (RV3.parents.has_key(RV2.name) and RV2.parents.has_key(RV1.name)):
					return self.solve_conditional_probability(RV1, RV2, r1s, r2s)


			# CASE 2
			# If RV1 (P) is conditionally dependent on evidence E given evidence Root
			# ex. P (P | c,s) 
			RVS_not_root = []
			RV_root_id = None

			for i in range(0, len(RV_arr)):
				if RV_arr[i] != RV_root:
					RVS_not_root.append(i)
				else:
					RV_root_id = i

			RV_root_parent_evidence_id = None

			if (RV_root_id == 2):
				RV_root_parent_evidence_id = 1
			else:
				RV_root_parent_evidence_id = 2

			if (r1s == "~"):
				probability = 1-RV1.marginal_probability
			else:
				probability = RV1.marginal_probability

			probability *= RV_root.probs.get(RV_status_arr[RVS_not_root[0]]+RV_arr[RVS_not_root[0]].marginal_probability_name+RV_status_arr[RVS_not_root[1]]+RV_arr[RVS_not_root[1]].marginal_probability_name, RV_root.probs.get(RV_status_arr[RVS_not_root[1]]+RV_arr[RVS_not_root[1]].marginal_probability_name+RV_status_arr[RVS_not_root[0]]+RV_arr[RVS_not_root[0]].marginal_probability_name, False))

			probability /= self.solve_conditional_probability(RV_root, RV_arr[RV_root_parent_evidence_id], RV_status_arr[RV_root_id], RV_status_arr[RV_root_parent_evidence_id])
			
		
			return probability


		elif reasoning[0] == COMBINED:
			# This is a special case in which 2 lowest nodes are present, representing a conditionally dependent combined reasoning
			# P (D | X, P) for example
			if isinstance(reasoning[1], tuple):

				RV_root_id1 = reasoning[1][0] - 1 #RV1
				RVparents = RV1.parents.values()
				rvp = RVparents[0] # also the parent of RV_root2

				RV_root_id2 = reasoning[1][1] - 1
				Root_RV = RV_arr[RV_root_id2]

				other_evidence_id = None
				if (RV_root_id2 == 1):
					other_evidence_id = 2
				elif (RV_root_id2 == 2):
					other_evidence_id = 1

				rv1_given_rvp = self.solve_conditional_probability(RV1, rvp, r1s, "")
				root_rv_given_rvp = self.solve_conditional_probability(Root_RV, rvp, RV_status_arr[RV_root_id2], "")
				rv1_given_not_rvp = self.solve_conditional_probability(RV1, rvp, r1s, "~")
				root_rv_given_not_rvp = self.solve_conditional_probability(Root_RV, rvp, RV_status_arr[RV_root_id2], "~")
				rvp_given_other_evidence = self.solve_conditional_probability(rvp, RV_arr[other_evidence_id], "", RV_status_arr[other_evidence_id])
				not_rvp_given_other_evidence = 1 - rvp_given_other_evidence
				root_rv_given_other_evidence = self.solve_conditional_probability(Root_RV, RV_arr[other_evidence_id], RV_status_arr[RV_root_id2], RV_status_arr[other_evidence_id])
				
				probability = (rv1_given_rvp * root_rv_given_rvp * rvp_given_other_evidence) + (rv1_given_not_rvp * root_rv_given_not_rvp * not_rvp_given_other_evidence)
				probability /= root_rv_given_other_evidence
				return probability

			# The default case for handling combined reasoning,
			RV_root_id = reasoning[1] - 1
			other_evidence_id = None
			if (RV_root_id == 2):
				other_evidence_id = 1
			elif (RV_root_id == 1):
				other_evidence_id = 2

			# Works by bayes theorem that we can calculate it out based on lowest node
			# P (Lowest Node | RV1, Not-LN)
			root_given_rvs = self.solve_conditional_on_joint_probability(RV_arr[RV_root_id], RV_arr[(RV_root_id+1)%3], RV_arr[(RV_root_id+2)%3], RV_status_arr[RV_root_id], RV_status_arr[(RV_root_id+1)%3], RV_status_arr[(RV_root_id+2)%3])
			
			# P (Lowest Node | Not-LN)
			root_given_other_evidence = self.solve_conditional_probability(RV_arr[RV_root_id], RV_arr[other_evidence_id], RV_status_arr[RV_root_id], RV_status_arr[other_evidence_id])
			
			# P (RV1 | Not-LN)
			probability = self.solve_conditional_probability(RV1, RV_arr[other_evidence_id], r1s, RV_status_arr[other_evidence_id])
			
			probability *= root_given_rvs
			probability /= root_given_other_evidence

			return probability


		elif reasoning[0] == NEITHER:
			RVparents = RV1.parents.values()
			rvp = RVparents[0]
			
			rv1_given_rvp = self.solve_conditional_probability(RV1, rvp, r1s, "")
			rv1_given_not_rvp = self.solve_conditional_probability(RV1, rvp, r1s, "~")
			rvp_given_rv2_rv3 = self.solve_conditional_on_joint_probability(rvp, RV2, RV3, "", r2s, r3s)
			not_rvp_given_rv2_rv3 = 1 - rvp_given_rv2_rv3

			probability = (rv1_given_rvp*rvp_given_rv2_rv3) + (rv1_given_not_rvp*not_rvp_given_rv2_rv3)
			probability /= (rvp_given_rv2_rv3+not_rvp_given_rv2_rv3)
			return probability
 

	def determine_reasoning_with_mult_evidence(self, RV1, RV2, RV3): # RV2 and RV3 are the evidence nodes, we determine the reasoning here based on their relationship

		# Check for obvious redundancy
		if (RV1 == RV2):
			return (INHERENTLY_GIVEN, 2)
		elif (RV1 == RV3):
			return (INHERENTLY_GIVEN, 3)

		# Check for Intercausal relationship
		if (RV2.parents.has_key(RV3.name)):
			return (INT_CAUS, RV2)
		elif (RV3.parents.has_key(RV2.name)):
			return (INT_CAUS, RV3)

		# Check for Combined relationship
		direction = self.decide_direction_of_reasoning(RV2, RV3)
		if (direction != SIBLING):
			if (len(RV1.children.items()) == 0 and len(RV3.children.items()) == 0):
				return (COMBINED, (1, 3))
			elif (len(RV1.children.items()) == 0 and len(RV2.children.items()) == 0):
				return (COMBINED, (1, 2))
			elif len(RV2.children.items()) == 0:
				return (COMBINED, 2) #RV will represent the lowest node in combined
			else:
				return (COMBINED, 3)

		# Neither, this case arises if P (x | p,s)
		return (NEITHER, None)


	def solve_joint_probability_three(self, RV1, RV2, RV3, r1s, r2s, r3s):

		#Fix this for all cases and handle chaining
		r1_given_r2r3 = self.solve_conditional_on_joint_probability(RV1, RV2, RV3, r1s, r2s, r3s)
		r2_given_r3 = self.solve_conditional_probability(RV2, RV3, r2s, r3s)
		result = RV3.marginal_probability * r1_given_r2r3 * r2_given_r3

		return result


	def lookup_node(self, a):
		for x in self.nodes.values():
			if (x.marginal_probability_name == a.upper()):
				return x
		print ("You asked to perform computation on a nonexistent node.")
		print ("Please try again with a correct bayes network query.")
		print "------------------------------------"
		print ""
		sys.exit(2)


	def bayes_network_query(self, flag, a):
		a = a.replace("/", "|")

		if flag == "-m":
			p = a.find("~")
			if len(a) > 1 and p == -1:
				print ("You cannot perform a -m on two variables.")
				print "------------------------------------"
				print ""
				sys.exit(2)

			result = None
			upper = a.isupper()
			
			if (upper):
				x = self.lookup_node(a)
				result = x.marginal_probability

				print "Marginal Probability Distribution of", a
				print a.lower()+":", result, "~"+a.lower()+":", 1-result
			else:			
				if "~" in a:
					x = self.lookup_node(a[1])
					result = 1-x.marginal_probability
				else:
					x = self.lookup_node(a)
					result = x.marginal_probability
				print "Marginal Probability of", a+":", result	

		elif flag == "-p":
			self.update_probability(a[0], float(a[1:]))
			print "New probability of", a[0].lower(), "=", float(a[1:])

		elif flag == "-g":

			variations = {}
			self.recurse_on_combinations(a, variations)
			for var_arg in variations.keys():
				self.conditional_helper(flag, var_arg)
			

		elif flag == "-j":

			variations = {}
			self.recurse_on_combinations(a, variations)
			for var_arg in variations.keys():
				self.joint_helper(flag, var_arg)


		else:
			assert False, "unhandled option"


	def recurse_on_combinations(self, a, memo_table):
		base_case = True
		for c in a:
			if c.isupper():
				b = a.replace(c, c.lower())
				c = a.replace(c, "~"+c.lower())
				if not memo_table.has_key(b):
					self.recurse_on_combinations(b, memo_table)
				if not memo_table.has_key(c):
					self.recurse_on_combinations(c, memo_table)
				base_case = False

		if (base_case):
			memo_table[a] = True


	def conditional_helper(self, flag, a):
		p = a.find("|")
		if (p == -1):
			print ("This is not a conditional probability.")
			print "------------------------------------"
			print ""
			sys.exit(2)

		rv1 = a[:p]
		rv1status = ""
		if "~" in rv1:
			rv1 = rv1[1]
			rv1status = "~"

		condition_on_rv_arr = []
		condition_on_rv_status_arr = []

		negate = False
		for char in a[p+1:]:
			if char == "~":
				negate = True
			else:
				condition_on_rv_arr.append(char)
				if negate == True:
					negate = False
					condition_on_rv_status_arr.append("~")
				else:
					condition_on_rv_status_arr.append("")
		
		if len(condition_on_rv_arr) == 1:
			RV1 = self.lookup_node(rv1)
			RV2 = self.lookup_node(condition_on_rv_arr[0])
			print "Probability of", a, "=", round(self.solve_conditional_probability(RV1, RV2, rv1status, condition_on_rv_status_arr[0]), 4)
		
		elif len(condition_on_rv_arr) == 2:
			RV1 = self.lookup_node(rv1)
			RV2 = self.lookup_node(condition_on_rv_arr[0])
			RV3 = self.lookup_node(condition_on_rv_arr[1])
			print "Probability of", a, "=", round(self.solve_conditional_on_joint_probability(RV1, RV2, RV3, rv1status, condition_on_rv_status_arr[0], condition_on_rv_status_arr[1]), 4)


	def joint_helper(self, flag, a):
		p = a.find("|")

		if p > -1:
			print ("This is not a joint probability.")
			print "------------------------------------"
			print ""
			sys.exit(2)

		#Handle upper case distributions yes?
		rv_arr = []
		rv_status_arr = []

		negate = False
		for char in a:
			if char == "~":
				negate = True
			else:
				rv_arr.append(char)
				if negate == True:
					negate = False
					rv_status_arr.append("~")
				else:
					rv_status_arr.append("")

		num_rvs = len(rv_arr)

		if num_rvs < 2 or num_rvs > 3:
			print ("Not a valid joint probability. Number of variables caused error.")
			print "------------------------------------"
			print ""
			sys.exit(2)
		elif num_rvs == 2:
			RV1 = self.lookup_node(rv_arr[0])
			RV2 = self.lookup_node(rv_arr[1])
			print "Probability of", a, "=", round(self.solve_joint_probability_pair(RV1, RV2, rv_status_arr[0], rv_status_arr[1]), 4)

		elif num_rvs == 3:
			RV1 = self.lookup_node(rv_arr[0])
			RV2 = self.lookup_node(rv_arr[1])
			RV3 = self.lookup_node(rv_arr[2])
			print "Probability of", a, "=", round(self.solve_joint_probability_three(RV1, RV2, RV3, rv_status_arr[0], rv_status_arr[1], rv_status_arr[2]), 4)



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
	P.add_child(C)
	C.add_parent(S)
	S.add_child(C)
	X.add_parent(C)
	C.add_child(X)
	D.add_parent(C)
	C.add_child(D)

	BN = Bayesian_Network()
	BN.add_node(P)
	BN.add_node(S)
	BN.add_node(C)
	BN.add_node(X)
	BN.add_node(D)
	BN.calculate_marginal_probabilities()

	return BN


FLAGS = ':g:j:m:p:'

if __name__ == "__main__":
	try:
		opts, args = getopt.getopt(sys.argv[1:], FLAGS)
	except getopt.GetoptError as err:
		print str(err)
		sys.exit(2)

	bayes_net = construct_bayes_net()
	print ""
	print "------------------------------------"
	for o, a in opts:
		bayes_net.bayes_network_query(o, a)
	print "------------------------------------"
	print ""
