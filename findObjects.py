objectFound = []

def updateObjectFound(items):
    global objectFound
    itemsNameFound = []
   
    for box in items.boxes:
        class_id = int(box.cls[0])  
        name = items.names[class_id]      
        itemsNameFound.append(name)
    
    objectFound = itemsNameFound

def getFoundObjects():
    return objectFound.copy()

def getObjectFound(items):
    foundItems = []
   
    for box in items.boxes:
        itemId = int(box.cls[0])  
        name = items.names[itemId]      
        foundItems.append(name)
        
    return foundItems

