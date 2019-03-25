# test.py

import numpy as np
import os
import tensorflow as tf
import cv2
import base64
from PIL import Image
from io import BytesIO
from scipy.misc import toimage

from utils import label_map_util
from utils import visualization_utils as vis_util
from distutils.version import StrictVersion

# module level variables ##############################################################################################
TEST_IMAGE_DIR = os.getcwd() +  "/test_images"
FROZEN_INFERENCE_GRAPH_LOC = os.getcwd() + "/inference_graph/frozen_inference_graph.pb"
LABELS_LOC = os.getcwd() + "/" + "label_map.pbtxt"
NUM_CLASSES = 2

#######################################################################################################################
#def main():
print("starting program . . .")

    # end if

    # this next comment line is necessary to avoid a false PyCharm warning
    # noinspection PyUnresolvedReferences
if StrictVersion(tf.__version__) < StrictVersion('1.5.0'):
    raise ImportError('Please upgrade your tensorflow installation to v1.5.* or later!')
    # end if

    # load a (frozen) TensorFlow model into memory
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(FROZEN_INFERENCE_GRAPH_LOC, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')
        # end with
    # end with

    # Loading label map
    # Label maps map indices to category names, so that when our convolution network predicts `5`, we know that this corresponds to `airplane`.  Here we use internal utility functions, but anything that returns a dictionary mapping integers to appropriate string labels would be fine
label_map = label_map_util.load_labelmap(LABELS_LOC)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                                use_display_name=True)
category_index = label_map_util.create_category_index(categories)
        # end if
    # end for
#testimg = open('test.jpg', 'rb')
#image_read = testimg.read()

#image_64_encode = base64.encodestring(image_read)
#print(type(image_64_encode))

def Object_Detection(b64String):
    with detection_graph.as_default():
        with tf.Session(graph=detection_graph) as sess:

            imgdata = base64.b64decode(b64String)

            theImage = Image.open(BytesIO(imgdata))
            b, g, r = theImage.split()
            Testimage = Image.merge("RGB", (r, g, b))
            image_np = np.array(Testimage)

                # Definite input and output Tensors for detection_graph
            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
                # Each box represents a part of the image where a particular object was detected.
            detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
                # Each score represent how level of confidence for each of the objects.
                # Score is shown on the result image, together with the class label.
            detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
            detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
            num_detections = detection_graph.get_tensor_by_name('num_detections:0')

                # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
            image_np_expanded = np.expand_dims(image_np, axis=0)
                # Actual detection.
            (boxes, scores, classes, num) = sess.run(
                [detection_boxes, detection_scores, detection_classes, num_detections],
                feed_dict={image_tensor: image_np_expanded})
                # Visualization of the results of a detection.



            vis_util.visualize_boxes_and_labels_on_image_array(image_np,
                                                                np.squeeze(boxes),
                                                                np.squeeze(classes).astype(np.int32),
                                                                np.squeeze(scores),
                                                                category_index,
                                                                use_normalized_coordinates=True,
                                                                line_thickness=8)
            buffered = BytesIO()
            im = Image.fromarray(image_np,"RGB")
            b, g, r = im.split()
            image = Image.merge("RGB", (r, g, b))
            image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue())
            if len([category_index.get(value) for index,value in enumerate(classes[0]) if scores[0,index] > 0.4]) > 0:
                theResults = {
                'name': [category_index.get(value) for index,value in enumerate(classes[0]) if scores[0,index] > 0.4][0]["name"],
                'accuracy': scores[0,0],
                'image': img_str
                }
            else:
                theResults = {
                'name': "No Result Detected",
                'accuracy': 0,
                'image': img_str
                }
            print("Finished Object Detection")
            return theResults
            # end for
        # end with
    # end with
    #Object_Detection(image_64_encode)
# end main

#Object_Detection(image_64_encode)
#######################################################################################################################
def checkIfNecessaryPathsAndFilesExist():
    if not os.path.exists(TEST_IMAGE_DIR):
        print('ERROR: TEST_IMAGE_DIR "' + TEST_IMAGE_DIR + '" does not seem to exist')
        return False
    # end if

    # ToDo: check here that the test image directory contains at least one image

    if not os.path.exists(FROZEN_INFERENCE_GRAPH_LOC):
        print('ERROR: FROZEN_INFERENCE_GRAPH_LOC "' + FROZEN_INFERENCE_GRAPH_LOC + '" does not seem to exist')
        print('was the inference graph exported successfully?')
        return False
    # end if

    if not os.path.exists(LABELS_LOC):
        print('ERROR: the label map file "' + LABELS_LOC + '" does not seem to exist')
        return False
    # end if

    return True
# end function

#######################################################################################################################
if __name__ == "__main__":
    main()
