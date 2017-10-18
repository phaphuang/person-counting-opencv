# import the necessary packages
import argparse
import datetime
import imutils
import time
import cv2
import pPerson
import numpy as np

# construct the argument parser and parse the arguments
"""
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())

# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
	camera = cv2.VideoCapture(0)
	time.sleep(0.25)

# otherwise, we are reading from a video file
else:
	camera = cv2.VideoCapture(args["video"])
"""

camera = cv2.VideoCapture('../src/mycctv01.avi')

# initialize the first frame in the video stream
firstFrame = None

INST_WIDTH = 800
INST_HEIGHT = 600
persons = []
### Input and Output Counters
cnt_up = 0
cnt_down = 0
font = cv2.FONT_HERSHEY_SIMPLEX
max_p_age = 5
pid = 1

### Line of up/down
line_up = int(2*(INST_HEIGHT/10))
line_down = int(3*(INST_HEIGHT/10))
#line_mid = (line_up + line_down) / 2
up_limit = int(1*(INST_HEIGHT/10))
down_limit = int(4*(INST_HEIGHT/10))

print "Blue line y:", str(line_down)
print "Red line y:", str(line_up)

line_down_color = (255,0,0)
line_up_color = (0,0,255)
# Point = [x, y]
# line_down
pt1 = [0, line_down]
pt2 = [INST_WIDTH, line_down]
pts_L1 = np.array([pt1,pt2], np.int32)
pts_L1 = pts_L1.reshape((-1,1,2))
# line_up
pt3 = [0, line_up];
pt4 = [INST_WIDTH, line_up];
pts_L2 = np.array([pt3, pt4], np.int32)
pts_L2 = pts_L2.reshape((-1,1,2))

pt5 = [0, up_limit]
pt6 = [INST_WIDTH, up_limit]
pts_L3 = np.array([pt5, pt6], np.int32)
pts_L3 = pts_L3.reshape((-1,1,2))
pt7 = [0, down_limit]
pt8 = [INST_WIDTH, down_limit]
pts_L4 = np.array([pt7, pt8], np.int32)
pts_L4 = pts_L4.reshape((-1,1,2))

if camera.isOpened():
    ret, image = camera.read()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, (INST_WIDTH, INST_HEIGHT))
    # Assign new height and width for ROI
    (xr, yr, wr, hr) = cv2.boundingRect(gray)
    startYROI = 2*hr/10
    endYROI = hr-5*hr/20
else:
    print "Camera is not open"

# loop over the frames of the video
while True:
	# grab the current frame and initialize the occupied/unoccupied
	# text
    (grabbed, frame) = camera.read()
    text = "Unoccupied"

	# if the frame could not be grabbed, then we have reached the end
	# of the video
    if not grabbed:
        break

	# resize the frame, convert it to grayscale, and blur it
    #frame = imutils.resize(frame, width=800)
    frame = cv2.resize(frame, (INST_WIDTH, INST_HEIGHT))
    cv2.rectangle(frame, (150, startYROI), (wr-300, endYROI), (0, 255, 0), 2)
    roi_image = frame[startYROI:endYROI, 150:wr-300]
    gray = cv2.cvtColor(roi_image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)


	# if the first frame is None, initialize it
    if firstFrame is None:
        firstFrame = gray
        continue

    # compute the absolute difference between the current frame and first frame
    frameDelta = cv2.absdiff(firstFrame, gray)

    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

    for i in persons:
        i.age_one()     # age every person one frame

	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    _, cnts, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # loop over the contours
    for cnt in cnts:
		# if the contour is too small, ignore it
		#if cv2.contourArea(c) < args["min_area"]:
        print cv2.contourArea(cnt)
        if cv2.contourArea(cnt) < 10000 or cv2.contourArea(cnt) > 30000:
            continue

		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
        else:

            M = cv2.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            xc,yc,wc,hc = cv2.boundingRect(cnt)

            new = True
            if cy in range(up_limit, down_limit):
                for i in persons:
                    ## Verify person which is the same as person who already detected before
                    if abs(xc-i.getX()) <= wc and abs(yc-i.getY()) <= hc:
                        new = False
                        i.updateCoords(cx, cy)  ##Update coordinate of person and reset age
                        if i.going_UP(line_down, line_up) == True:
                            cnt_up += 1;
                            print "ID:", i.getId(), 'crossed going up at', time.strftime("%c")
                        elif i.going_DOWN(line_down, line_up) == True:
                            cnt_down += 1;
                            print "ID:", i.getId(), 'crossed going down at', time.strftime("%c")
                        break

                    if i.getState() == '1':
                        if i.getDir() == 'down' and i.getY() > down_limit:
                            i.setDone()
                        elif i.getDir() == 'up' and i.getY() < up_limit:
                            i.setDone()

                    if i.timedOut():
                        ### remove from the person list
                        index = persons.index(i)
                        persons.pop(index)
                        del i   # free memory

                if new == True:
                    p = pPerson.MyPerson(pid, cx, cy, max_p_age)
                    persons.append(p)
                    pid += 1
            ################
            #   DRAWING    #
            ################
            #(x, y, w, h) = cv2.boundingRect(cnt)
            cv2.circle(roi_image, (cx, cy), 5, (0,0,255), -1)
            cv2.rectangle(roi_image, (xc, yc), (xc + wc, yc + hc), (0, 255, 0), 2)
            text = "Occupied"

    #############################
    #   DRAWING TRAJECTORIES    #
    #############################
    for i in persons:
        #if len(i.getTracks()) >= 2:
        #    pts = np.array(i.getTracks(), np.int32)
        #    pts = pts.reshape((-1,1,2))
        #    frame = cv2.polylqines(frame, [pts], False, i.getRGB())
        #if i.getId() == 9:
        #    print str(i.getX()), ',', str(i.getY())
        cv2.putText(roi_image, str(i.getId()), (i.getX(), i.getY()), font, 0.3, i.getRGB(), 1, cv2.LINE_AA)

    #############
    #   IMAGES  #
    #############
    str_up = 'UP: ' + str(cnt_up)
    str_down = 'DOWN: ' + str(cnt_down)
    cv2.polylines(roi_image, [pts_L1], False, line_down_color, thickness=2)
    cv2.polylines(roi_image, [pts_L2], False, line_up_color, thickness=2)
    # line limit
    cv2.polylines(roi_image, [pts_L3], False, (255,255,255), thickness=1)
    cv2.polylines(roi_image, [pts_L4], False, (255,255,255), thickness=1)
    cv2.putText(roi_image, str_up, (10,40), font, 0.5, (255,255,255), 2, cv2.LINE_AA)
    cv2.putText(roi_image, str_up, (10,40), font, 0.5, (0,0,255), 1, cv2.LINE_AA)
    cv2.putText(roi_image, str_down, (10,90), font, 0.5, (255,255,255), 2, cv2.LINE_AA)
    cv2.putText(roi_image, str_down, (10, 90), font, 0.5, (255,0,0), 1, cv2.LINE_AA)

    # draw the text and timestamp on the frame
    cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

	# show the frame and record if the user presses a key
    cv2.imshow("Security Feed", roi_image)
    cv2.imshow("Thresh", thresh)
    cv2.imshow("Frame Delta", frameDelta)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break


# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
