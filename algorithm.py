import json

def lot_alg(lot):
    result = [True]
    for text in lot["rateCard"]:
        if (text == "Customers Only: Free"):
            result[0] = False
            break
    result.append(lot["distance"])
    if (lot["calculatedRates"] == None):
        result.append(0)
    else:
        result.append(lot["calculatedRates"][0]["rateCost"])
    result.append(lot["spacesTotal"])
    for x in result:
        if (x == None):
            result[0] = False
    if (not(result[2]>0)):
        result[0] = False
    #if 0 index is 0, lot is not valid
    #index 1 is distance, 2 is cost, 3 is spots theoretically open
    return result

def lots_analyze(lots):
    lotsInfo = []
    for lot in lots["result"]:
        lotsInfo.append(lot_alg(lot))
    return lotsInfo

def check_conditions(lot,distance,cost,spots):
    if (lot[0] == True and 
        lot[1] <= distance and
        lot[2] <= cost and 
        lot[3] >= spots):
        return True
    else:
        return False

def distanceFunct(e):
    return e[1]
def costFunct(e):
    return e[2]
def scoreFunct(e):
    #ADJUST SCORING HERE
    return 0.6*e[1] + 0.3*e[2] + 0.1*e[3]
def format_list(lotsList, distance, cost, spots):
    rawList = lots_analyze(lotsList)
    refinedList = []
    for list in rawList:
        if (check_conditions(list, distance, cost, spots)):
            refinedList.append(list) 
    """         
    if (sortby == "distance"):
        refinedList.sort(key=distanceFunct)
    elif (sortby == "cost"):
        refinedList.sort(key=costFunct)
    else:
        refinedList = None
    """
    refinedList.sort(key=scoreFunct)
    return refinedList
    
    #return filteredList

sampleLots={}
with open ("C:\\Users\\seant\\Downloads\\response_1701555881322.json","r") as f:
    sampleLots = json.load(f)
sampleLot=sampleLots["result"][7]
#print (sampleLot)
formatted_list = format_list(sampleLots, 2000, 50, 1)
print(formatted_list)
#testList = [lot_alg(sampleLot), [True, 1500, 30, 5]]
#print(testList.sort(key = distanceFunct))
    