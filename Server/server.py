# USAGE
# python server.py --prototxt MobileNetSSD_deploy.prototxt --model MobileNetSSD_deploy.caffemodel --montageW 2 --montageH 2

# import the necessary packages
from imutils import build_montages
from datetime import datetime
import numpy as np
import imagezmq
import argparse
import imutils
import cv2

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


lock = threading.Lock()

# initialize a flask object
app = Flask(__name__)




frameDict = {}

# initialize the dictionary which will contain  information regarding
# when a device was last active, then store the last time the check
# was made was now
lastActive = {}
lastActiveCheck = datetime.now()


@app.route("/")
def index():
	# return the rendered template
	return render_template("index.html")



def generate():


	# loop over frames from the output stream
	while True:

		(rpiName, frame) = imageHub.recv_image()


		imageHub.send_reply(b'OK')


		#frame = imutils.resize(frame, width=500)

		if frame is None:
			continue

		# encode the frame in JPEG format
		(flag, encodedImage) = cv2.imencode(".jpg", frame)

		# ensure the frame was successfully encoded
		if not flag:
			continue

		# yield the output frame in the byte format
		yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
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
	app.run(host="35.184.217.161", port=8000, debug=True,
			threaded=True, use_reloader=False)

# do a bit of cleanup
cv2.destroyAllWindows()