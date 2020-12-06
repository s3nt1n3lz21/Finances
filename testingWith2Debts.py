import calculateDebts
import pprint

A0 = 1500
B0 = 1500
calculateDebts.setMonthlyPayment(500)
calculateDebts.setPossibleCombinations(calculateDebts.calculatePossibleCombinations(2))
calculateDebts.setMonthlyInterestRates([1.02,1.10])
calculateDebts.calculateChildNodeDebts([A0,B0],[])
pprint.pprint(calculateDebts.bestSolution)