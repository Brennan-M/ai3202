##########################################
#		   Bayes Net Sampling	 		 #
#	       Brennan McConnell		 	 #
##########################################

class Bayesian_Network(object):

	def __init__(self):
		self.cloudy = {"C":0.5}
		self.sprinkler = {"C":0.1, "~C":0.5}
		self.rain = {"C":0.8, "~C":0.2}
		self.wetgrass = {"SR":0.99, "~SR":0.90, "S~R":0.90, "~S~R":0.00}
		self.sampleValues = [0.82, 0.56, 0.08, 0.81, 0.34, 0.22, 0.37, 0.99, 0.55, 0.61, 0.31, 0.66, 0.28, 1.0, 0.95, 0.71, 0.14, 0.1, 1.0, 0.71, 0.1, 0.6, 0.64, 0.73, 0.39, 0.03, 0.99, 1.0, 0.97, 0.54, 0.8, 0.97, 0.07, 0.69, 0.43, 0.29, 0.61, 0.03, 0.13, 0.14, 0.13, 0.4, 0.94, 0.19, 0.6,	0.68, 0.36,	0.67,	0.12, 0.38, 0.42, 0.81, 0.0, 0.2, 0.85, 0.01, 0.55, 0.3, 0.3, 0.11,	0.83, 0.96, 0.41, 0.65,	0.29, 0.4, 0.54, 0.23, 0.74, 0.65, 0.38, 0.41, 0.82, 0.08, 0.39, 0.97,	0.95, 0.01, 0.62, 0.32,	0.56, 0.68, 0.32, 0.27, 0.77, 0.74, 0.79, 0.11, 0.29, 0.69, 0.99, 0.79,	0.21, 0.2, 0.43, 0.81, 0.9, 0.0, 0.91, 0.01]

	def performProbability(self, cloudS, sprinklerS, rainS, wetgrassS):

		if cloudS < self.cloudy["C"]:
			cloudy = True
			cloudVal = "C"
		else:
			cloudy = False
			cloudVal = "~C"

		if sprinklerS < self.sprinkler[cloudVal]:
			sprinkVal = "S"
			sprinkler = True
		else:
			sprinkVal = "~S"
			sprinkler = False

		if rainS < self.rain[cloudVal]:
			rainVal = "R"
			rain = True
		else:
			rainVal = "~R"
			rain = False

		if wetgrassS < self.wetgrass[sprinkVal+rainVal]:
			wetgrass = True
		else:
			wetgrass = False

		return (cloudy, sprinkler, rain, wetgrass)

	def run(self):
		samples = []
		for i in range(0, 100, 4):
			samples.append(self.performProbability(self.sampleValues[i],self.sampleValues[i+1],self.sampleValues[i+2],self.sampleValues[i+3]))
		return samples


if __name__ == "__main__":
	BN = Bayesian_Network()
	results = BN.run()

	cloudyTrueCount = 0.0
	cloudyGivenRainCount = 0.0
	sprinklerGivenWetCount = 0.0
	sprinklerGivenCandWCount = 0.0
	for (c, s, r, w) in results:
		if c == True:
			cloudyTrueCount += 1
		if r == True:
			if c == True:
				cloudyGivenRainCount += 1
		if w == True:
			if s == True:
				sprinklerGivenWetCount += 1
		if c == True and w == True:
			if s == True:
				sprinklerGivenCandWCount += 1

	print "P(c=True): ", cloudyTrueCount/len(results)

	print "P(c=True | r=True): ", cloudyGivenRainCount/len(results)

	print "P(s=True | w=True): ", sprinklerGivenWetCount/len(results)

	print "P(s=True | c=True,w=True): ", sprinklerGivenCandWCount/len(results)




