import json

def lot_alg(lot):
    result = [{"valid":True, "walkTime":0, "rawData":lot}]
    for text in lot["rateCard"]:
        if (text == "Customers Only: Free"):
            result[0]["valid"] = False
            break
    result.append(lot["distance"])
    if (lot["calculatedRates"] == None):
        result.append(0)
    else:
        result.append(lot["calculatedRates"][0]["rateCost"])
    result.append(lot["spacesTotal"])
    for x in result:
        if (x == None):
            result[0]["valid"] = False
    if (not(result[2]>0)):
        result[0]["valid"] = False
    #if 0 index is 0, lot is not valid
    #index 1 is distance, 2 is cost, 3 is spots theoretically open
    return result

def lots_analyze(lots):
    lotsInfo = []
    for lot in lots["result"]:
        lotsInfo.append(lot_alg(lot))
    return lotsInfo

def check_conditions(lot,distance,cost,spots):
    if (lot[0]["valid"] == True and 
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
    return 0.6*e[1] + 0.3*e[2] + 0.1*e[3] + 0.0*e[0]["walkTime"]
def format_list(lotsList, walkTimeList, distance, cost, spots):
    rawList = lots_analyze(lotsList)
    for index in range(0,len(walkTimeList)-1):
        rawList[index][0]["walkTime"] = walkTimeList[index]
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
walkTimeList = [207, 108, 101, 89, 94, 57, 193, 96, 117, 122, 128,
                206, 40, 150, 106, 172, 202, 47, 188, 81, 181, 41, 
                77, 134, 119, 126, 129, 34, 43, 53, 159, 132, 204, 
                120, 182, 80, 77, 163, 42, 186, 145, 142, 181]
formatted_list = format_list(sampleLots, walkTimeList, 2000, 50, 1)
#print(formatted_list)
#testList = [lot_alg(sampleLot), [True, 1500, 30, 5]]
#print(testList.sort(key = distanceFunct))
printString = "["
for log in formatted_list:
    printString = printString + "[" + str(log[1]) + ", " + str(log[2]) + ", " + str(log[3]) + "] "
printString = printString + "]"
print(printString)

    