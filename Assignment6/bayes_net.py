##########################################
#		Bayes Net Disease Predictor		 #
#			Brennan McConnell			 #
##########################################

class Node(object):

	def __init__(self, name, cpn):
		self.name = name
		self.probs = {}
		self.parents = {}
		self.children = {}
		self.conditional_prob_calculated = False
		self.conditional_probability_name = cpn
		self.conditional_probability = None

	def add_probability(self, key, value):
		self.probs[key] = value

	def add_parent(self, node):
		self.parents[node.name] = node

	def add_child(self, node):
		self.children[node.name] = node


class Bayesian_Network(object):

	def __init__(self):
		self.nodes = {}

	def add_node(self, node):
		self.nodes[node.name] = node

	def calculate_marginal_probabilities(self):
		for RV in self.nodes.values():
			if RV.conditional_prob_calculated == False:
				self.solve_marginal_prob(RV)

	def solve_marginal_prob(self, RV):
		if (len(RV.parents) == 0):
			results = RV.probs.values()
			if (len(results) != 1):
				print "ERROR FOUND!"
			else:
				RV.conditional_probability = results[0]
				RV.conditional_prob_calculated = True
		else:
			RV_cond_prob = 0.0
			rvp_cond_probs = {}
			for rvp in RV.parents.values():
				if (rvp.conditional_prob_calculated == False):
					self.solve_marginal_prob(rvp)
				rvp_cond_probs[rvp.conditional_probability_name] = rvp.conditional_probability

			for (key, val) in RV.probs.items():
				cur = 1.0
				negate = False
				for char in key:
					if (char == '~'):
						negate = True
					else:
						if (negate == False):
							cur *= rvp_cond_probs[char]
						else:
							negate = False
							cur *= (1 - rvp_cond_probs[char])
				RV_cond_prob += val * cur

			RV.conditional_probability = RV_cond_prob
			RV.conditional_prob_calculated = True


def construct_bayes_net():
	P = Node("Pollution", "P")
	P.add_probability("L", 0.9)
	S = Node("Smoker", "S")
	S.add_probability("T", 0.3)
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

	P.add_child(C)
	S.add_child(C)
	C.add_child(X)
	C.add_child(D)
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

	return BN

def query_bayes_net(query):
	parse_query(query)


if __name__ == "__main__":
	bayes_net = construct_bayes_net()
	for node in bayes_net.nodes.values():
		print (node.conditional_probability_name, " : ", node.conditional_probability)









