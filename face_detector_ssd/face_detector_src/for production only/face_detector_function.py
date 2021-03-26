# import the necessary packages
import numpy as np
import cv2

# defining prototext and caffemodel paths
caffeModel = "../face_detector_model/face_model/res10_300x300_ssd_iter_140000.caffemodel"
prototextPath = "../face_detector_model/face_model/deploy.prototxt"

# Load Model
print("Loading model...................")
net = cv2.dnn.readNetFromCaffe(prototextPath,caffeModel)

def face_detector(image):
    face_boxes = dict()
    confidence = dict()

    # extract the original dimensions
    (h,w) = image.shape[:2]
    # Resize image to 300x300 and 
    # convert image into blobFromImage
    # blobImage convert RGB (104.0, 177.0, 123.0)
    blob = cv2.dnn.blobFromImage(cv2.resize(
                                image,(300,300)),
                                1.0,(300,300),
                                (104.0, 177.0, 123.0))

    # passing blob through the network to detect and predict
    net.setInput(blob)
    detections = net.forward()

    # loop over the detections
    for i in range(0, detections.shape[2]):
        # extract the confidence and prediction
        confid_all = detections[0, 0, i, 2]

        # filter detections by confidence greater than the minimum
        if confid_all < 0.5:
            continue
        # compute the (x, y)-coordinates of the bounding box for the
        # object
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        #print(confid_all)
        (startX, startY, endX, endY) = box.astype("int")
        startX -= 15
        startY -= 15
        endX += 15
        endY += 15
        startX = max(0, startX)
        startY = max(0, startY)
        endX = max(0, endX)
        endY = max(0, endY)

        # Save confidence and coordinates for each detected face
        confidence[i] = confid_all
        face_boxes[i] = (startX, startY, endX, endY)

    return face_boxes, confidence






'''

        # draw the bounding box of the face along Confidance
        # probability
        text = "{:.2f}%".format(confidence * 100)
        y = startY - 10 if startY - 10 > 10 else startY + 10
        cv2.rectangle(image, (startX, startY), (endX, endY),
                    (0, 0, 255), 2)
        cv2.putText(image, text, (startX, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

'''