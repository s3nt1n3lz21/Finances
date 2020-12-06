import math
import random

earliestSolutionNodeDepth = 99999
bestSolution = []
possibleCombinations = [[0.3,0.7],[0.7,0.3]]
monthlyPayment = 500
monthlyInterests = [1.02,1.03]
noTimesNoSolution = [0 for i in range(100)]

def loop(i,currentFractions,validCombinations,possibleFractions,numDebts):
    for fraction in possibleFractions:
        if i == 1:
            # If setting the last value, set it to 1-sum(rest)
            currentFractions[i-1] = round(1-sum(currentFractions),1)
            combination = [currentFractions[j] for j in range(numDebts)]
            validCombinations.append(combination)
            # Skip the rest of this loop and checking higher numbers for this index as sum will only be greater than 1
            currentFractions[i-1] = 0.0
            break
        else:
            # Otherwise set it to the next value
            currentFractions[i-1] = fraction
        # If sum is already one skip changing the lower index numbers as sum will only be greater than 1
        if abs(sum(currentFractions) - 1) < 0.01:
            combination = [currentFractions[j] for j in range(numDebts)]
            validCombinations.append(combination)
            # Skip the rest of this loop and checking higher numbers for this index as sum will only be greater than 1
            currentFractions[i-1] = 0.0
            break
        else:
            loop(i-1,currentFractions,validCombinations,possibleFractions,numDebts)

def calculatePossibleCombinations(numDebts):
    validCombinations = []
    currentFractions = [0 for i in range(numDebts)]
    possibleFractions = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
    loop(numDebts,currentFractions,validCombinations,possibleFractions,numDebts)
    return validCombinations

def setMonthlyPayment(payment):
    global monthlyPayment
    monthlyPayment = payment

def setPossibleCombinations(combiantions):
    global possibleCombinations
    possibleCombinations = combiantions
    random.shuffle(possibleCombinations)

def setMonthlyInterestRates(interestRates):
    global monthlyInterests
    monthlyInterests = interestRates

def subtractPayment(debt,payment):
    if debt > payment:
        debt -= payment
        payment = 0
    else:
        payment -= debt
        debt = 0
    return [debt,payment]

# subtract the payments from the debts. Put money towards the next debt if one is already paid.
def subtractPayments(debts, combination):
    paymentLeftOver = 0
    
    # Subtract the payment from the debt and get the payment left over
    for i in range(len(debts)):
        [debts[i], paymentLeftOver] = subtractPayment(debts[i],combination[i]*monthlyPayment+paymentLeftOver)

#      e.g.
#     [debtA, paymentLeftOver] = subtractPayment(debtA,mA*monthlyPayment+paymentLeftOver)
#     [debtB, paymentLeftOver] = subtractPayment(debtB,mB*monthlyPayment+paymentLeftOver)        

    # Put the left over payments to the other debts
    for i in range(len(debts)):
        [debts[i], paymentLeftOver] = subtractPayment(debts[i],paymentLeftOver)
        
#      e.g. 
#     [debtA, paymentLeftOver] = subtractPayment(debtA,paymentLeftOver)
#     [debtB, paymentLeftOver] = subtractPayment(debtB,paymentLeftOver)

    return debts

# Apply interest to all the debts
def applyInterest(debts):
    for i in range(len(debts)):
        debts[i] *= monthlyInterests[i]
    
    return debts

def resetNoTimesNoSolution(depth):
    global noTimesNoSolution
    # reset noTimesNoSolution[depth] and lower depths to 0
    for i in range(depth,len(noTimesNoSolution)):
        noTimesNoSolution[i] = 0

# For each node go through all the possible child nodes
# At each node we will have a list of the history of debts and fractions and add to it as we go down the tree
# debts - Pass in the current values of debts [debtA,debtB]
# combinationsAndDebtsOverTime e.g [[combination, debts],[combination,debts],...] - Pass in the current history of the debts over time going down this node
def calculateChildNodeDebts(debts,combinationsAndDebtsOverTime):
    global bestSolution
    global earliestSolutionNodeDepth
    global possibleCombinations
    global noTimesNoSolution
    
    thisNodeDepth = len(combinationsAndDebtsOverTime)+1
    oldSumDebts = sum(debts[:])
    # If still not found a solution after 100 months checking this node tree don't check any further and check the other nodes
    if thisNodeDepth > 100:
        return
    
    for combination in possibleCombinations:

        # If there have been 10 failures to find a solution at the next depth skip checking the rest of this node
        # and increase the number of failures at this node depth by 1
        if noTimesNoSolution[thisNodeDepth+1] == 10:
            noTimesNoSolution[thisNodeDepth] += 1
            resetNoTimesNoSolution(thisNodeDepth+1)
            return

        # Skip checking this node if already found a solution at shorter node depths or at this depth.
        # We only want to find better solutions at shorter depths
        if len(bestSolution) <= thisNodeDepth and len(bestSolution) > 0:
            return

        # Skip checking earlier nodes if no solution has been found at a depth one less than the best solution depth
        # if thisNodeDepth <= len(bestSolution) - 1 and thisNodeDepth > 0:
        #     return
        
        currentCombinationsAndDebtsOverTime = combinationsAndDebtsOverTime[:]
        currentDebts = debts[:]

        # Subtract the payments from the debts
        currentDebts = subtractPayments(currentDebts,combination)

        # Apply interest to the debts
        currentDebts = applyInterest(currentDebts)
        
        # Add the current debts and fractions to the history for the next child node
        combinationsAndDebts = [combination, currentDebts]
        
        currentCombinationsAndDebtsOverTime.append(combinationsAndDebts)
        
        # print(thisNodeDepth)

        # Check sum of debts is zero
        if abs(sum(currentDebts) - 0) < 0.01:
            # If sum of debts is zero stop checking the child nodes and add the set the best solution
            # print('found a solution: ', currentCombinationsAndDebtsOverTime[:])

            # Reset the best solution
            bestSolution = currentCombinationsAndDebtsOverTime
            # print('bestSolution: ', currentCombinationsAndDebtsOverTime[:])
            # print('len(bestSolution): ', len(bestSolution))
            # print('found a better solution')
            return
        else:
            # Don't check further down the tree if the sum of the debts is increasing faster than the monthly payment
            if sum(currentDebts) > oldSumDebts + monthlyPayment:
                # print('sum increasing too quick')
                # print('noTimesNoSolution: ', noTimesNoSolution)
                # print(str(sum(currentDebts)) + ' > ' + str(oldSumDebts) + ' + ' + str(monthlyPayment))
                noTimesNoSolution[thisNodeDepth] += 1
                return

            # Go further down the node tree only if the best solution is at a depth lower than the next one
            if len(bestSolution) == 0 or len(bestSolution) > thisNodeDepth+1:
                calculateChildNodeDebts(currentDebts[:],currentCombinationsAndDebtsOverTime[:])
    return