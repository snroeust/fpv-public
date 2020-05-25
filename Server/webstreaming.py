# USAGE
# python webstreaming.py --ip 0.0.0.0 --port 8000

# import the necessary packages
# from pyimagesearch.motion_detection import SingleMotionDetector
from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
import threading
import argparse
import datetime
import imutils
import time
import cv2
from imutils import build_montages
from datetime import datetime
import numpy as np
import imagezmq
import argparse
import imutils
import cv2

# initialize the ImageHub object
imageHub = imagezmq.ImageHub()

# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful for multiple browsers/tabs
# are viewing tthe stream)
outputFrame = None
lock = threading.Lock()

# initialize a flask object
app = Flask(__name__)

# initialize the video stream and allow the camera sensor to
# warmup
# vs = VideoStream(usePiCamera=1).start()
vs = VideoStream(src=0).start()
time.sleep(2.0)


@app.route("/")
def index():
	# return the rendered template
	return render_template("index.html")




def generate():
	# grab global references to the output frame and lock variables
	global outputFrame, lock

	# loop over frames from the output stream
	while True:
		# receive RPi name and frame from the RPi and acknowledge
		# the receipt
		(rpiName, frame) = imageHub.recv_image()
		imageHub.send_reply(b'OK')

		# if a device is not in the last active dictionary then it means
		# that its a newly connected device
		# if rpiName not in lastActive.keys():
		# print("[INFO] receiving data from {}...".format(rpiName))

		# record the last active time for the device from which we just
		# received a frame
		# lastActive[rpiName] = datetime.now()

		# resize the frame to have a maximum width of 400 pixels, then
		# grab the frame dimensions and construct a blob
		frame = imutils.resize(frame, width=400)







		with lock:
			# check if the output frame is available, otherwise skip
			# the iteration of the loop
			if frame is None:
				continue

			# encode the frame in JPEG format
			(flag, encodedImage) = cv2.imencode(".jpg", frame)

		# ensure the frame was successfully encoded
		# if not flag:
		# continue

		# yield the output frame in the byte format
		yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
			   bytearray(encodedImage) + b'\r\n')


@app.route("/video_feed")
def video_feed():
	# return the response generated along with the specific media
	# type (mime type)
	return Response(generate(),
					mimetype="multipart/x-mixed-replace; boundary=frame")


# check to see if this is the main thread of execution
if __name__ == '__main__':


	# start the flask app
	app.run(host="127.0.0.1", port=8000, debug=True,
			threaded=True, use_reloader=False)

# release the video stream pointer
vs.stop()








