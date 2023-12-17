import cv2
import os
import csv
writer = csv.writer( open('test.csv', 'w', newline = '') )
fields = ['filename','class','width', 'height','xmin','ymin','xmax','ymax']
writer.writerow(fields)
for i in os.listdir(r'images'):
	if i != "desktop.ini":
		image = cv2.imread (f"images/{i}")
		cv2.imshow("image", image)
		marker = cv2.selectROI("image", image, fromCenter=False, showCrosshair=True)
		marker = list(marker)
		#append xmax
		marker.append(marker[0]+marker[2])
		#append ymax
		marker.append(marker[1]+marker[3])
		#insert filepath and class at the beggining
		marker.insert(0,i)
		marker.insert(1, "watch")
		print(f"images/{i},{marker}")
		writer.writerow(marker)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
