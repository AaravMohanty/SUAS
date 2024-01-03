import json
from pprint import pprint
def convert_bbox_to_polygon(bbox):
    x = bbox[0]
    y = bbox[1]
    w = bbox[2]
    h = bbox[3]
    polygon = [x,y,(x+w),y,(x+w),(y+h),x,(y+h)]
    return([polygon])
def main():
    file_path = "ValidateCOCO.json"
    f = open(file_path)
    data = json.load(f)
    for line in data["annotations"]:
        segmentation = convert_bbox_to_polygon(line["bbox"])
        line["segmentation"] = segmentation
    with open("validatecocosegmentation.json", 'w') as f:
        f.write(json.dumps(data))
    print('DONE')
main()
