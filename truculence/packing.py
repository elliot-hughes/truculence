import math
import numpy

def squareness(factors):
	if isinstance(factors, int):
		factors = factorize(factors)[-1]
	d = len(factors)
	w = numpy.prod(factors)**(1/float(d))		# This is the weight to apply to the factors in order to make the product 1.
	return 1-(w/max(factors))**d		# Between 0 (square) and 1 (line). NOTE: THIS DOESN'T REALLY HOLD FOR d > 2 ...
	
	# This is a slightly different version of squareness which runs from 0 to infinity:
#	return (max(factors) - min(factors))/w

def factorize(n):		# To do: extend to "d" factors instead of just pairs
	return [(i, n/i) for i in range(1, int(n**0.5) + 1) if n % i == 0]
