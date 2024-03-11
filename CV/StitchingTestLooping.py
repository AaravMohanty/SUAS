import shutil
import cv2 
import os
# initialized a list of images 
imgs = [] 

validOutput: cv2.typing.MatLike = None
stitchy = cv2.Stitcher.create(cv2.STITCHER_SCANS)

stitching_batch_size = 1

output_path = "stitching_results"
os.makedirs(output_path, exist_ok=True)
for filename in os.listdir(output_path):
    file_path = os.path.join(output_path, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

for filename in os.listdir('stitching_test_imgs'): 
    print(f"Reading image: {filename}")
    img = cv2.imread('stitching_test_imgs/' + filename)
    if img is not None:
        print(f"Successfully read image: {filename}")
    else:
        print(f"Reading image failed: {filename}")
        break
    imgs.append(img)

    if len(imgs) >= stitching_batch_size:
        print("--- Attempting to stitch images... ---")
        try:
            (dummy,output) = stitchy.stitch(imgs)
        except RuntimeError as e:
            print(f"err: {e}")
            # cv2.imshow('result', output)
            # cv2.waitKey(0)
            continue
        if dummy != cv2.STITCHER_OK:
            if dummy == cv2.Stitcher_ERR_NEED_MORE_IMGS:
                print(f"Stitching failed: need more imgs")
            else:
                print(f"Stitching failed: {dummy}")
        elif output is None:
            print(f"⚠ Stitching returned no output.")
        if dummy == cv2.STITCHER_OK and output is not None:
            # replace the old images with the new stitched image
            shape = output.shape
            # newOut = cv2.resize(validOutput, (int(.1*shape[1]), int(.1*shape[0])))
            imgs = [output]
            # cv2.imshow('result', newOut)
            
            ok = cv2.imwrite(os.path.join(output_path, filename), output)
            if ok:
                print(f"😊 Stitched image: {filename}")
                validOutput = output
            else:
                print(f"Failed to write stitched image, did you forget to create the directory?: {filename}")
            # cv2.waitKey(0)


"""
stitchy=cv2.Stitcher.create(cv2.STITCHER_PANORAMA)
(dummy,output) = stitchy.stitch(imgs)
cv2.imshow('result', output)

if dummy != cv2.STITCHER_OK: 
  # checking if the stitching procedure is successful 
  # .stitch() function returns a true value if stitching is  
  # done successfully 
    print("stitching failed") 
else:  
    print('result:') 
"""
# final output
# cv2.imwrite("result.jpg", validOutput)
finalshape = validOutput.shape
resizedOut = cv2.resize(validOutput, (int(.1*finalshape[1]), int(.1*finalshape[0])))
cv2.imshow('final result', resizedOut)

cv2.waitKey(0)