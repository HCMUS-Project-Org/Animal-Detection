# import package
import os 
import base64

try:
    import cv2
except:
    os.system('pip install opencv-python')
    import cv2

try:
    import numpy as np
except:
    os.system('pip install numpy')
    import numpy as np

try:
    import eel

except:
    os.system('pip install eel')
    import eel

# -- define global var --
whTarget = 320
confThreshold = 0.5
mnsThreshold = 0.3
color = (0,255,0)
detectedImgPath = 'Static/picture/result.jpg'
# classFiles = '../config/object.names'
# colorFiles = '../config/object.colors'
# modelConfig = '../config/animal.cfg'
# modelWeights = '../config/animal_last.weights'
classFiles = '../config/coco.names'
modelConfig = '../config/yolov3.cfg'
modelWeights = '../config/yolov3.weights'
weights_url = 'https://pjreddie.com/media/files/yolov3.weights'
# -- init Directory containt html --
eel.init('Static')

# -- download weight -- 
# isExist = os.path.isfile(modelWeights)
# if isExist == False:
#     wget 


# -- read class name --
classNames = []     
with open(classFiles, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

# -- Give the configuration and weight files for the model and load the network. --
net = cv2.dnn.readNetFromDarknet(modelConfig, modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)


def readImage(img_b64): # read image and convert it to blob
    # https://stackoverflow.com/questions/33754935/read-a-base-64-encoded-image-from-memory-using-opencv-python-library
    encoded_data = img_b64.split(',')[1]
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)

    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    blob = cv2.dnn.blobFromImage(img, 1/255, (whTarget, whTarget), [0, 0, 0], 1, crop= False)

    return img, blob


def findObject(outputs, img):
    hT, wT, cT = img.shape
    boundingBox = []
    classIds = []
    confidences = []

    for output in outputs:
        for detection in output:
            scores = detection[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            
            if confidence > confThreshold:
                w, h = int(detection[2]*wT), int(detection[3]*hT)
                # center point
                x, y = int(detection[0]*wT - w/2), int(detection[1]*hT - h/2)
                boundingBox.append([x, y, w, h])
                classIds.append(classId)
                confidences.append(float(confidence))

    print('bb:',len(boundingBox))
    
    indices = cv2.dnn.NMSBoxes(boundingBox, confidences, confThreshold,mnsThreshold)
    print(indices)


    for i in indices:
        print(i)
        try:
            i = i[0]
        except:
            pass 

        box = boundingBox[i]
        x, y, w, h = box[0], box[1], box[2], box[3] 
        cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
        cv2.putText(img,f'{classNames[classIds[i]].upper()} {int(confidences[i]*100)}%', (x + 5, y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

# export function for js use
@eel.expose
def animalDetection(img_b64):
    img, blob = readImage(img_b64)

    # input blob into network
    net.setInput(blob)

    # determine the output layer
    layerNames = net.getLayerNames()

    try:
        outputNames = [layerNames[i[0]-1] for i in net.getUnconnectedOutLayers()]
    except:
        outputNames = [layerNames[i-1] for i in net.getUnconnectedOutLayers()]

    # get ouput from forward propagation
    outputs = net.forward(outputNames)

    findObject(outputs, img)

    # save detected img
    cv2.imwrite(detectedImgPath, img)



# -- start Desktop app --
eel.start('index.html', size=(1000, 520))