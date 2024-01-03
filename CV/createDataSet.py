import cv2,os,csv,json
import numpy as np
import pandas as pd
from pprint import pprint
#constants
csvpath = 'datasets/CSV/validateWatch.csv'
cocopath = 'datasets/COCO/validateWatch.json'
with open(csvpath, 'w',newline = '') as file:
    writer = csv.writer(file)
    fields = ['filename','class','width', 'height','xmin','ymin','xmax','ymax']
    writer.writerow(fields)
    for i in os.listdir(r'images'):
        if i != "desktop.ini":
            image = cv2.imread (f"images/{i}")
            cv2.namedWindow("Image", cv2.WINDOW_NORMAL)

            cv2.imshow("Image",image)
            marker = cv2.selectROI("Image", image, fromCenter=False, showCrosshair=True)
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

data = pd.read_csv(csvpath)

images = []
categories = []
annotations = []

category = {}
category["supercategory"] = 'none'
category["id"] = 0
category["name"] = 'None'
categories.append(category)

data['fileid'] = data['filename'].astype('category').cat.codes
data['categoryid']= pd.Categorical(data['class'],ordered= True).codes
data['categoryid'] = data['categoryid']+1
data['annid'] = data.index

def image(row):
    image = {}
    image["height"] = row.height
    image["width"] = row.width
    image["id"] = row.fileid
    image["file_name"] = row.filename
    return image

def category(row):
    category = {}
    category["supercategory"] = 'None'
    category["id"] = row.categoryid
    category["name"] = row[2]
    return category

def annotation(row):
    annotation = {}
    area = (row.xmax -row.xmin)*(row.ymax - row.ymin)
    annotation["segmentation"] = []
    annotation["iscrowd"] = 0
    annotation["area"] = area
    annotation["image_id"] = row.fileid

    annotation["bbox"] = [row.xmin, row.ymin, row.xmax -row.xmin,row.ymax-row.ymin ]

    annotation["category_id"] = row.categoryid
    annotation["id"] = row.annid
    return annotation

for row in data.itertuples():
    annotations.append(annotation(row))

imagedf = data.drop_duplicates(subset=['fileid']).sort_values(by='fileid')
for row in imagedf.itertuples():
    images.append(image(row))

catdf = data.drop_duplicates(subset=['categoryid']).sort_values(by='categoryid')
for row in catdf.itertuples():
    categories.append(category(row))

data_coco = {}
data_coco["images"] = images
data_coco["categories"] = categories
data_coco["annotations"] = annotations
json.dump(data_coco, open(cocopath, "w"), indent=4)



def convert_bbox_to_polygon(bbox):
    x = bbox[0]
    y = bbox[1]
    w = bbox[2]
    h = bbox[3]
    polygon = [x,y,(x+w),y,(x+w),(y+h),x,(y+h)]
    return([polygon])

f = open(cocopath)
data = json.load(f)
for line in data["annotations"]:
    segmentation = convert_bbox_to_polygon(line["bbox"])
    line["segmentation"] = segmentation
with open(cocopath, 'w') as f:
    f.write(json.dumps(data))
print('DONE')