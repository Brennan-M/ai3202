##############################
# Hidden Markov Model Part 1 #
#	   Brennan McConnell	 #
##############################

import sys

TRANSITION = 0
EMISSION = 1
MARGINAL = 2

class HMM(object):

	def __init__(self):
		self.states = {}
		for i in range(97, 123):		
			self.states[chr(i)] = ({}, {}, {})
		self.states["_"] = ({}, {}, {})

	def buildFromData(self, fileName):
		f = open(fileName)
		infoArr = []
		for line in f:
			infoArr.append((line[0], line[2]))
	
		# Emission Probabilities
		for state in self.states.keys():

			stateCount = 0.0
			outputCount = {}
			transitionCount = {}

			for i in range(0, len(infoArr) - 1):
				if (infoArr[i][0] == state):
					stateCount += 1

					# Emission Probabilities
					if outputCount.has_key(infoArr[i][1]):
						outputCount[infoArr[i][1]] += 1
					else:
						outputCount[infoArr[i][1]] = 1


					# Transition Probabilities
					if transitionCount.has_key(infoArr[i+1][0]):
						transitionCount[infoArr[i+1][0]] += 1
					else:
						transitionCount[infoArr[i+1][0]] = 1


			for s1 in self.states.keys():
				if not self.states[state][EMISSION].has_key(s1):
					self.states[state][EMISSION][s1] = round(1.0/(stateCount+27), 5)

			for s2 in self.states.keys():
				if not self.states[state][TRANSITION].has_key(s2):
					self.states[state][TRANSITION][s2] = round(1.0/(stateCount+27), 5)


			for key, value in outputCount.items():
				self.states[state][EMISSION][key] = round((value+1)/(stateCount+27), 5)

			for key, value in transitionCount.items():
				self.states[state][TRANSITION][key] = round((value+1)/(stateCount+27), 5)

			self.states[state][MARGINAL][state] = round(stateCount/len(infoArr), 5)


	def printHMM(self):
		print "---------------------------------------"

		print "\n"
		print "Marginal Probabilities"
		print "---------------------------------------"
		for state in self.states.keys():
			print "P(", state, ") = ", self.states[state][MARGINAL][state]

		print "\n"
		print "Emission Probabilities"
		print "---------------------------------------"
		sortedResults = []
		for state in self.states.keys():
			for evidence, value in self.states[state][EMISSION].items():
				string = "P( " + evidence + " | " + state + " ) = " + str(value)
				sortedResults.append(string)

		for line in sorted(sortedResults, key=lambda x: x[4]):
			print line

		print "\n"
		print "Transition Probabilities"
		print "---------------------------------------"
		sortedResults = []
		for state in self.states.keys():
			for stateNext, value in self.states[state][TRANSITION].items():
				string = "P( " + stateNext + " | " + state + " ) = " + str(value)
				sortedResults.append(string)

		for line in sorted(sortedResults, key=lambda x: x[4]):
			print line

		print "\n"
		print "---------------------------------------"




if __name__ == "__main__":
	hmm = HMM()
	fname = sys.argv[1]
	hmm.buildFromData(fname)
	hmm.printHMM()








