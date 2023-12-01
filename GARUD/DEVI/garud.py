'''

                                                      GARUD - THE WATCHER
               Inspired rom "Garutmantha (or) Garudmantha - The watcher of the realms" according to Hindu Puranas
         Garuda is a obect detection sotware which can detect objects in the real time live stream or from a recorded video
'''


import numpy as np
import argparse
import imutils
import time
import cv2
import os
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import pyttsx3
engine = pyttsx3.init()

root=Tk()
root.geometry('570x570')
root.resizable(width=False, height=False)
root.title('Garud')
root.config(background='papaya whip')
##label = Label(root, text="garud",bg='aquamarine',font=('helvetica 30 bold'))
##label.pack(side=TOP)

filename = PhotoImage(file="garudback.png")
background_label = Label(root,image=filename)
background_label.pack(side=TOP)

filename2 = PhotoImage(file="gar.png")
background_label2 = Label(root,image=filename2)
background_label2.place(x=220,y=0)

statusbar=Label(root,width=60,text="A Project by Team SAHARA",font=("arial",13,"bold"),bg="black",fg="white",relief=SUNKEN)
statusbar.place(x=0,y=550)


def destroy():
   root.destroy()


ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", 
	help="path to output video",default='output.avi')
ap.add_argument("-y", "--yolo",
	help="base path to YOLO directory",default='yolo-coco')
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
ap.add_argument("-t", "--threshold", type=float, default=0.3,
	help="threshold when applyong non-maxima suppression")
args = vars(ap.parse_args())

# load the COCO class labels our YOLO model was trained on
labelsPath = os.path.sep.join([args["yolo"], "coco.names"])
LABELS = open(labelsPath).read().strip().split("\n")

# initialize a list of colors to represent each possible class label
np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
	dtype="uint8")

# derive the paths to the YOLO weights and model configuration
weightsPath = os.path.sep.join([args["yolo"], "yolov3.weights"])
configPath = os.path.sep.join([args["yolo"], "yolov3.cfg"])

# load our YOLO object detector trained on COCO dataset (80 classes)
# and determine only the *output* layer names that we need from YOLO
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# initialize the video stream, pointer to output video file, and

# frame dimensions
def live():
        vs = cv2.VideoCapture(0)
        writer = None
        (W, H) = (None, None)

        while True:
                # read the next frame from the file
                grabbed, frame = vs.read()
                # if the frame was not grabbed, then we have reached the end
                # of the stream
                if not grabbed:
                        break

                # if the frame dimensions are empty, grab them
                if W is None or H is None:
                        (H, W) = frame.shape[:2]

                # construct a blob from the input frame and then perform a forward
                # pass of the YOLO object detector, giving us our bounding boxes
                # and associated probabilities
                blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
                        swapRB=True, crop=False)
                net.setInput(blob)
                start = time.time()
                layerOutputs = net.forward(ln)
                end = time.time()

                # initialize our lists of detected bounding boxes, confidences,
                # and class IDs, respectively
                boxes = []
                confidences = []
                classIDs = []

                # loop over each of the layer outputs
                for output in layerOutputs:
                        # loop over each of the detections
                        for detection in output:
                                # extract the class ID and confidence (i.e., probability)
                                # of the current object detection
                                scores = detection[5:]
                                classID = np.argmax(scores)
                                confidence = scores[classID]

                                # filter out weak predictions by ensuring the detected
                                # probability is greater than the minimum probability
                                if confidence > args["confidence"]:
                                        # scale the bounding box coordinates back relative to
                                        # the size of the image, keeping in mind that YOLO
                                        # actually returns the center (x, y)-coordinates of
                                        # the bounding box followed by the boxes' width and
                                        # height
                                        box = detection[0:4] * np.array([W, H, W, H])
                                        (centerX, centerY, width, height) = box.astype("int")

                                        # use the center (x, y)-coordinates to derive the top
                                        # and and left corner of the bounding box
                                        x = int(centerX - (width / 2))
                                        y = int(centerY - (height / 2))

                                        # update our list of bounding box coordinates,
                                        # confidences, and class IDs
                                        boxes.append([x, y, int(width), int(height)])
                                        confidences.append(float(confidence))
                                        classIDs.append(classID)

                # apply non-maxima suppression to suppress weak, overlapping
                # bounding boxes
                idxs = cv2.dnn.NMSBoxes(boxes, confidences, args["confidence"],
                        args["threshold"])
                l=[]

                # ensure at least one detection exists
                if len(idxs) > 0:
                        # loop over the indexes we are keeping
                        for i in idxs.flatten():
                                # extract the bounding box coordinates
                                (x, y) = (boxes[i][0], boxes[i][1])
                                (w, h) = (boxes[i][2], boxes[i][3])

                                # draw a bounding box rectangle and label on the frame
                                color = [int(c) for c in COLORS[classIDs[i]]]
                                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                                text = "{}: {:.2f}".format(LABELS[classIDs[i]],
                                        confidences[i])
                                cv2.putText(frame, text, (x, y - 5),
                                        cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
                                l.append(LABELS[classIDs[i]])
                        if cv2.waitKey(1) &0xFF==ord('s'):
                           for i in range(len(l)):
                              
                              res=l[i]
                              engine.say(res)
                              engine.runAndWait()
                           l.clear()
                                   
                # check if the video writer is None
                if writer is None:
                        # initialize our video writer
                        fourcc = cv2.VideoWriter_fourcc(*"MJPG")
                        writer = cv2.VideoWriter(args["output"], fourcc, 11,
                                (frame.shape[1], frame.shape[0]), True)
                cv2.imshow("Garud is watching... Press 'Esc' to close",frame)
                writer.write(frame)
                k = cv2.waitKey(30) & 0xff
                if k==27:break
        writer.release()
        vs.release()
        cv2.destroyAllWindows()



def vid():
        filename = filedialog.askopenfilename(initialdir =  "/", title = "Select A File", filetype =
        (("video files","*.mp4"),("all files","*.*")) )

        vs = cv2.VideoCapture(filename)
        writer = None
        (W, H) = (None, None)

        # try to determine the total number of frames in the video file
        try:
                prop = cv2.cv.CV_CAP_PROP_FRAME_COUNT if imutils.is_cv2() \
                        else cv2.CAP_PROP_FRAME_COUNT
                total = int(vs.get(prop))
                print("[INFO] {} total frames in video".format(total))

        # an error occurred while trying to determine the total
        # number of frames in the video file
        except:
                print("[INFO] could not determine # of frames in video")
                print("[INFO] no approx. completion time can be provided")
                total = -1

        # loop over frames from the video file stream
        while True:
                # read the next frame from the file
                (grabbed, frame) = vs.read()

                # if the frame was not grabbed, then we have reached the end
                # of the stream
                if not grabbed:
                        break

                # if the frame dimensions are empty, grab them
                if W is None or H is None:
                        (H, W) = frame.shape[:2]

                # construct a blob from the input frame and then perform a forward
                # pass of the YOLO object detector, giving us our bounding boxes
                # and associated probabilities
                blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
                        swapRB=True, crop=False)
                net.setInput(blob)
                start = time.time()
                layerOutputs = net.forward(ln)
                end = time.time()

                # initialize our lists of detected bounding boxes, confidences,
                # and class IDs, respectively
                boxes = []
                confidences = []
                classIDs = []

                # loop over each of the layer outputs
                for output in layerOutputs:
                        # loop over each of the detections
                        for detection in output:
                                # extract the class ID and confidence (i.e., probability)
                                # of the current object detection
                                scores = detection[5:]
                                classID = np.argmax(scores)
                                confidence = scores[classID]

                                # filter out weak predictions by ensuring the detected
                                # probability is greater than the minimum probability
                                if confidence > args["confidence"]:
                                        # scale the bounding box coordinates back relative to
                                        # the size of the image, keeping in mind that YOLO
                                        # actually returns the center (x, y)-coordinates of
                                        # the bounding box followed by the boxes' width and
                                        # height
                                        box = detection[0:4] * np.array([W, H, W, H])
                                        (centerX, centerY, width, height) = box.astype("int")

                                        # use the center (x, y)-coordinates to derive the top
                                        # and and left corner of the bounding box
                                        x = int(centerX - (width / 2))
                                        y = int(centerY - (height / 2))

                                        # update our list of bounding box coordinates,
                                        # confidences, and class IDs
                                        boxes.append([x, y, int(width), int(height)])
                                        confidences.append(float(confidence))
                                        classIDs.append(classID)

                # apply non-maxima suppression to suppress weak, overlapping
                # bounding boxes
                idxs = cv2.dnn.NMSBoxes(boxes, confidences, args["confidence"],
                        args["threshold"])
                l=[]

                # ensure at least one detection exists
                if len(idxs) > 0:
                        # loop over the indexes we are keeping
                        for i in idxs.flatten():
                                # extract the bounding box coordinates
                                (x, y) = (boxes[i][0], boxes[i][1])
                                (w, h) = (boxes[i][2], boxes[i][3])

                                # draw a bounding box rectangle and label on the frame
                                color = [int(c) for c in COLORS[classIDs[i]]]
                                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                                text = "{}: {:.4f}".format(LABELS[classIDs[i]],
                                        confidences[i])
                                cv2.putText(frame, text, (x, y - 5),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                                l.append(LABELS[classIDs[i]])
                        if cv2.waitKey(1) &0xFF==ord('s'):
                           for i in range(len(l)):
                              
                              res=l[i]
                              engine.say(res)
                              engine.runAndWait()
                           l.clear()


                # check if the video writer is None
                if writer is None:
                        # initialize our video writer
                        fourcc = cv2.VideoWriter_fourcc(*"MJPG")
                        writer = cv2.VideoWriter(args["output"], fourcc, 11,
                                (frame.shape[1], frame.shape[0]), True)

                        # some information on processing single frame
                        if total > 0:
                                elap = (end - start)
                                print("[INFO] single frame took {:.4f} seconds".format(elap))
                                print("[INFO] estimated total time to finish: {:.4f}".format(elap * total))
                                n='Oops! video takes longer than expected. Video and will be processed and saved in '+"{:.2f}".format(elap * total)+'sec, Please be patient'
                                messagebox.showinfo("Information",n)

                # write the output frame to disk
                writer.write(frame)

        # release the file pointers
        print("[INFO] cleaning up...")
        messagebox.showinfo("Information","Video processed and saved as output.avi in project folder")
        writer.release()
        vs.release()



b1=Button(root,padx=5,pady=5,width=12,bg='white',fg='black',relief=GROOVE,command=live,text='Live Object',font=('helvetica 15 bold'),activebackground='light green')
b1.place(x=200,y=200)
b2=Button(root,padx=5,pady=5,width=12,bg='white',fg='black',relief=GROOVE,command=vid,text='Select video file',font=('helvetica 15 bold'),activebackground='light green')
b2.place(x=200,y=325)
b3=Button(root,padx=5,pady=5,width=12,bg='white',fg='black',relief=GROOVE,text='EXIT',command=destroy,font=('helvetica 15 bold'),activebackground='red')
b3.place(x=200,y=450)


root.mainloop()

