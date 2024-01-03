from mmdet.apis import init_detector, inference_detector
import mmcv

# Specify the path to model config and checkpoint file
config_file = '/home/rpi/mmdetection/configs/Config.py'
checkpoint_file = '/home/rpi/mmdetection/work_dirs/Config/epoch_12.pth'

# build the model from a config file and a checkpoint file
model = init_detector(config_file, checkpoint_file, device='cpu')

# test a single image and show the results
img = 'images/IMG_1764.jpg'  # or img = mmcv.imread(img), which will only load it once
result = inference_detector(model, img)
# visualize the results in a new window
#model.show_result(img, result)
# or save the visualization results to image files
model.show_result(img, result, out_file='result.jpg')
