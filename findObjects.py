objectFound = []

def updateObjectFound(items):
    global objectFound
    itemsNameFound = []
    
    if items is None or not hasattr(items, 'boxes') or len(items.boxes) == 0:
        objectFound = []
        return
   
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

def getItemCanBeFind():
    itemsNames = [
  'airplane',
  'apple',
  'backpack',
  'baseball bat',
  'baseball glove',
  'banana',
  'bear',
  'bed',
  'bench',
  'bicycle',
  'bird',
  'boat',
  'book',
  'bottle',
  'bowl',
  'broccoli',
  'bus',
  'cake',
  'car',
  'carrot',
  'cat',
  'cell phone',
  'chair',
  'clock',
  'couch',
  'cow',
  'cup',
  'dining table',
  'dog',
  'donut',
  'elephant',
  'fire hydrant',
  'fork',
  'frisbee',
  'giraffe',
  'hair drier',
  'handbag',
  'horse',
  'hot dog',
  'keyboard',
  'kite',
  'knife',
  'laptop',
  'microwave',
  'motorcycle',
  'mouse',
  'orange',
  'oven',
  'parking meter',
  'person',
  'pizza',
  'potted plant',
  'refrigerator',
  'remote',
  'sandwich',
  'scissors',
  'sheep',
  'sink',
  'skis',
  'skateboard',
  'snowboard',
  'spoon',
  'sports ball',
  'stop sign',
  'suitcase',
  'surfboard',
  'teddy bear',
  'tennis racket',
  'tie',
  'toilet',
  'toaster',
  'toothbrush',
  'traffic light',
  'train',
  'truck',
  'tv',
  'umbrella',
  'vase',
  'wine glass',
  'zebra',
]
    return itemsNames