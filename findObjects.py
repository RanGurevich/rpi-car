def getObjectFound(items):
    detected_names = []
   
    for box in items.boxes:
        class_id = int(box.cls[0])  
        name = items.names[class_id]      
        detected_names.append(name)
        
    return detected_names

