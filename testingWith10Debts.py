import calculateDebts
import pprint

calculateDebts.setMonthlyPayment(19000)
calculateDebts.setPossibleCombinations(calculateDebts.calculatePossibleCombinations(10))
# print(len(calculateDebts.calculatePossibleCombinations(10)))
calculateDebts.setMonthlyInterestRates([1.3,1.1,1.3,1.3,1.2,1.3,1.3,1.3,1.3,2])
calculateDebts.calculateChildNodeDebts([5000,5000,5000,5000,5000,5000,5000,5000,5000,5000],[])
pprint.pprint(calculateDebts.bestSolution)
