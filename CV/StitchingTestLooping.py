import shutil
import cv2 
import os, glob

# Curr problems:
# - oodles of invalid images (bad rotation, use some image rotating library to normalize rotation using EXIF metadata)
# - with too large a buffer, stitching implodes on itself (unavoidable)

# Potential things:
# - Using pitch, yaw, roll to adjust/normalize images, maybe fix stitching
# - get technical, adjust parameters of opencv stitcher to make it fit our needs better

# using glob.glob, could switch to shutil (but more complicated)
# wipe prior results folder from previous run
# glob.glob gets all files in folder stitching_results
# can't call os.remove when empty, try catch call
try:
    for filename in glob.glob('stitching_results'):
        os.remove(filename)
# os.remove throws a PermissionError when folder is empty already
except PermissionError as e:
    print("stitching_results already clear!")

# initialize a list of images encoded as cv2 matlikes
imgs = []

# shape of previous object, stored as tuple
prevShape: tuple = (0, 0)

validOutput: cv2.typing.MatLike = None
stitchy = cv2.Stitcher.create(cv2.STITCHER_SCANS)

# amount of images to process at once
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

# go thru all images in test_imgs
for filename in os.listdir('stitching_test_imgs'): 
    # read images, add to imgs
    print(f"Reading image: {filename}")
    img = cv2.imread('stitching_test_imgs/' + filename)
    if img is not None:
        print(f"Successfully read image: {filename}")
    else:
        print(f"Reading image failed: {filename}")
        break
    imgs.append(img)

    if len(imgs) >= stitching_batch_size:
        print(len(imgs))
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

        # added condition that the current shape is greater than the old one
        # serves as a mitigation for the overwriting issue, preventing current image from overwriting
        # composite one by checking if current one is smaller than the composite
        # Doesn't actually use the image; instead trashes it
        # seek alternative although this may not be an issue in real world testing
        if dummy == cv2.STITCHER_OK and output is not None and output.shape[0] >= prevShape[0]:

            # replace the old images with the new stitched image
            imgs = [output]
            # cv2.imshow('result', newOut)
            prevShape = output.shape
            
            ok = cv2.imwrite(os.path.join(output_path, filename), output)
            if ok:
                print(f"😊 Stitched image: {filename}")
                validOutput = output
            else:
                print(f"Failed to write stitched image, did you forget to create the directory?: {filename}")
            # cv2.waitKey(0)
        else:
            if(len(imgs) > 10):
                # oldest unstitched image
                print("Popped image!")
                imgs.pop(1)

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