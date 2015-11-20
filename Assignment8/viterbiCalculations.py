##############################
# Hidden Markov Model Part 2 #
#	   Brennan McConnell	 #
##############################

from hmmBuilder import HMM
import math


class viterbi(object):

	def __init__(self, sampleData, fileCorrecting):
		self.hmm = HMM()
		self.hmm.buildFromData(sampleData)
		self.marginal, self.emission, self.transition = self.hmm.persistHMM()
		self.actualStates, self.observations = self.parseFileCorrecting(fileCorrecting)
		self.beforeAndAfterStates = self.observations
		self.correctedText = None
	
	def parseFileCorrecting(self, filename):
		f = open(filename, "r")
		actualStates = []
		observations = []

		for line in f:
			if " " in line:
				lineSplit = line.split(" ")
				actualStates.append(lineSplit[0])
				observations.append(lineSplit[1][0])

		f.close()
		return actualStates, observations


	def determineProbableSequence(self):

		self.beforeAndAfterStates = []

		pathProbabilities = [{}]
		path = {}

		states = []
		for i in range(ord("a"), ord("z") + 1):
			states.append(chr(i))
		states.append("_")

		# Calculate Initial Probabilities
		for state in states:
			# V( (t = 0) , X(0) ) = P( E(0) | X(0) ) * P(state) 
			# Use logs since numbers can potentially be very small
			pathProbabilities[0][state] = ( 
							math.log(self.emission[(self.observations[0], state)])
							+ math.log(self.marginal[state]))
			path[state] = state


		
		for obs in range(1, len(self.observations)): # Number of states we have
			updatedPath = {}
			pathProbabilities.append({})

			# V( (t), X(t) ) = P( E(t) | X(t) ) * P( X(t) | X(t-1) ) * V( (t-1), X(t-1))
			for curState in states:
				stateProbs = {}
				for prevState in states:
					stateProbs[prevState] = (
							math.log(self.emission[(self.observations[obs], curState)])
						  + math.log(self.transition[(curState, prevState)]) 
						  + pathProbabilities[obs-1][prevState]
						)
				nextState = max(stateProbs, key = stateProbs.get)
				probOfNextState = stateProbs[nextState]

				pathProbabilities[obs][curState] = probOfNextState
				updatedPath[curState] = path[nextState] + curState
			path = updatedPath
			


		finalState = max(pathProbabilities[len(pathProbabilities)-1], key = pathProbabilities[len(pathProbabilities)-1].get)

		correctedText = path[finalState]
		correctedText = correctedText.replace("_", " ")

		for char in path[finalState]:
			self.beforeAndAfterStates.append(char)

		self.correctedText = correctedText



	def calculateErrorRate(self):
		
		mismatches = 0.0
		for i in range(0, len(self.beforeAndAfterStates) - 1):
			if self.beforeAndAfterStates[i] != self.actualStates[i]:
				mismatches += 1
		return mismatches/len(self.beforeAndAfterStates)


if __name__ == "__main__":
	V = viterbi("typos20.data", "typos20Test.data")
	initialErrors = V.calculateErrorRate()
	V.determineProbableSequence()
	resultingErrors = V.calculateErrorRate()

	print "Starting Error Rate:", initialErrors
	print "Final Error Rate:", resultingErrors
	print "\n\n"
	print "Final Output..."
	print "--------------------------------------------------"
	print "\n\n"
	print V.correctedText	










