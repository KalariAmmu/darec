from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2
import pandas as pd

ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type=str, default="barcodes.csv",
	help="path to output CSV file containing barcodes")
args = vars(ap.parse_args())

print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

csv = open(args["output"], "w")
csv.write("{},{},{},{}\n".format('time','br_code','name','roll_no'))
found = set()
true_list = pd.read_csv('students.csv')

while True:

	frame = vs.read()
	frame = imutils.resize(frame, width=400)

	barcodes = pyzbar.decode(frame)

	for barcode in barcodes:
		(x, y, w, h) = barcode.rect
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

		barcodeData = barcode.data.decode("utf-8")
		barcodeType = barcode.type

		text = "{} ({})".format(barcodeData, barcodeType)
		cv2.putText(frame, text, (x, y - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

		if barcodeData not in found and barcodeData in true_list['br_code'].tolist():
			student=true_list[true_list['br_code']==barcodeData]
			csv.write("{},{},{},{}\n".format(datetime.datetime.now(),
				barcodeData,student['name'][0],student['roll_no'][0]))
			csv.flush()
			found.add(barcodeData)

	cv2.imshow("Barcode Scanner", frame)
	key = cv2.waitKey(1) & 0xFF

	if key == ord("q"):
		break

csv.close()
cv2.destroyAllWindows()
vs.stop()
