import cv2
import numpy as np
import tensorflow as tf
import json
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util


class TOD(object):
    def __init__(self):
        self.PATH_TO_CKPT = 'output/frozen_inference_graph.pb'
        self.PATH_TO_LABELS = 'data/object-detection.pbtxt'
        self.NUM_CLASSES = 14
        self.detection_graph = self._load_model()
        self.category_index = self._load_label_map()

    def _load_model(self):
        detection_graph = tf.Graph()
        with detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(self.PATH_TO_CKPT, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')
        return detection_graph

    def _load_label_map(self):
        label_map = label_map_util.load_labelmap(self.PATH_TO_LABELS)
        categories = label_map_util.convert_label_map_to_categories(label_map,
                                                                    max_num_classes=self.NUM_CLASSES,
                                                                    use_display_name=True)
        category_index = label_map_util.create_category_index(categories)
        return category_index

    #I have changed a lot
    def detect(self, image):
        with self.detection_graph.as_default():
            with tf.Session(graph=self.detection_graph) as sess:
                # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                image_np_expanded = np.expand_dims(image, axis=0)
                image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
                boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
                scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
                classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
                num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')
                # Actual detection.
                (boxes, scores, classes, num_detections) = sess.run(
                    [boxes, scores, classes, num_detections],
                    feed_dict={image_tensor: image_np_expanded})
                # Visualization of the results of a detection.
                vis_util.visualize_boxes_and_labels_on_image_array(
                    image,
                    np.squeeze(boxes),
                    np.squeeze(classes).astype(np.int32),
                    np.squeeze(scores),
                    self.category_index,
                    use_normalized_coordinates=True,
                    line_thickness=8)

        #if you want see the box with iamge please use this
        #cv2.namedWindow("detection", cv2.WINDOW_NORMAL)
        #cv2.imshow("detection", image)
        #cv2.waitKey(0)

        #date response
        classes = np.squeeze(classes).astype(np.int32)
        scores = np.squeeze(scores)
        boxes = np.squeeze(boxes)
         
        threshold = 0.5  #CWH: set a minimum score threshold of 10%
        obj_above_thresh = sum(n > threshold for n in scores)
        #print("detected %s objects in %s above a %s score" % ( obj_above_thresh, image, threshold))
        
        output = []
 
        #Add some metadata to the output
        for c in range(0, len(classes)):
          if scores[c] > threshold:
              class_name = self.category_index[classes[c]]['name']
              size= image.shape
              im_height=size[0]
              im_width =size[1]
              x_c=boxes[c][0]*im_width
              y_c=boxes[c][1]*im_height
              h_c=boxes[c][2]*im_height
              w_c=boxes[c][3]*im_width
              sc=int(scores[c]*100)/100


#              print(" object %s is a %s - score: %s, location: %s" % (c, class_name, scores[c], boxes[c]))
              item = [ { 'class name' : class_name, 'scores' :float(sc) , 'x' : int(x_c), 'y' : int(y_c), 'height' : int(h_c) , 'width' : int(w_c)} ]
#              item=[]
              #item.append(class_name)
              #item.append(float(scores[c]))
              #item.append(float(boxes[c][0]))
              #item.append(float(boxes[c][1]))
              #item.append(float(boxes[c][2]))
              #item.append(float(boxes[c][3]))
              output.append(item)
        #print(output)
        return output
        #outputJson = json.dumps(output)
        #return outputJson


def check(img_url):
    image = cv2.imread(img_url)
    detecotr = TOD()
    dete_o = detecotr.detect(image)
    return dete_o

#if __name__ == '__main__':
#    check()
