



def getCrytKey():
    return "NDSUTMK\L^"




def getRatio():
    data = []
    cryptData = getCrytKey()
    for x in range(len(cryptData)):
        if x%2!=0:
            data.append(ord(cryptData[x]))
        else:
            data.append(cryptData[x])


    return data
