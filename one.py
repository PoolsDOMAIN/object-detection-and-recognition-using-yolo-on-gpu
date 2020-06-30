# import the necessary packages
from imutils.video import FPS
import numpy as np
import argparse
import cv2
import os
# construct the argument parse and parse the arguments




# load the COCO class labels our YOLO model was trained on

LABELS = open("coco.names").read().strip().split("\n")
# initialize a list of colors to represent each possible class label
np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
	dtype="uint8")

# derive the paths to the YOLO weights and model configuration


# load our YOLO object detector trained on COCO dataset (80 classes)
print("[INFO] loading YOLO from disk...")
net = cv2.dnn.readNetFromDarknet("yolov3.cfg", "yolov3.weights")


def video(paths,gpu,conf,thresh,outpath):
	# check if we are going to use GPU
	if gpu:
		# set CUDA as the preferable backend and target
		print("[INFO] setting preferable backend and target to CUDA...")
		net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
		net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
	for path in paths:
		list1= path.split("/")
		listt=list1[-1].split('.')
		name=listt[0]
		


		# determine only the *output* layer names that we need from YOLO
		ln = net.getLayerNames()
		ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
		# initialize the width and height of the frames in the video file
		W = None
		H = None
		# initialize the video stream and pointer to output video file, then
		# start the FPS timer
		
		
		print("[INFO] accessing video stream...")
		vs = cv2.VideoCapture(path)
		writer = None
		fps = FPS().start()
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
			layerOutputs = net.forward(ln)

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
					if confidence > conf:
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
			idxs = cv2.dnn.NMSBoxes(boxes, confidences,conf,
				thresh)
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

			# check to see if the output frame should be displayed to our
			# screen
	#		if 1 > 0:
				# show the output frame
	#			cv2.imshow("Frame", frame)
	#			key = cv2.waitKey(1) & 0xFF
				# if the `q` key was pressed, break from the loop
	#			if key == ord("q"):
	#				break
			# if an output video file path has been supplied and the video
			# writer has not been initialized, do so now
			temp=outpath+"/"+name+".avi"
			
			if outpath != "" and writer is None:
				# initialize our video writer
				fourcc = cv2.VideoWriter_fourcc(*"MJPG")
				writer = cv2.VideoWriter(temp, fourcc, 30,
					(frame.shape[1], frame.shape[0]), True)
			# if the video writer is not None, write the frame to the output
			# video file
			if writer is not None:
				writer.write(frame)
			# update the FPS counter
			fps.update()
		# stop the timer and display FPS information
		fps.stop()
		print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
		print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
		

