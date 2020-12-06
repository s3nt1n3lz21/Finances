import calculateDebts

A0 = 5000
B0 = 4000
C0 = 3000
calculateDebts.setMonthlyPayment(1000)
calculateDebts.setPossibleCombinations(calculateDebts.calculatePossibleCombinations(3))
calculateDebts.setMonthlyInterestRates([1.02,1.03,1.025])
calculateDebts.calculateChildNodeDebts([A0,B0,C0],[])
print(calculateDebts.bestSolution)
print(len(calculateDebts.calculatePossibleCombinations(3)))