import cv2
from ultralytics import YOLO
from tqdm import tqdm
import numpy as np
from datetime import datetime


class CVDetector:
    def __init__(
            self,
            detection_model_checkpoint,
            classification_model_checkpoint,
            logger,
            visualise=False
        ):
        if not detection_model_checkpoint:
            raise ValueError("Error: Detection model checkpoint is not set in the environment variables.")
        if not classification_model_checkpoint:
            raise ValueError("Error: Classification model checkpoint is not set in the environment variables.")
        
        self.detection_model = YOLO(detection_model_checkpoint, verbose=False)
        # self.classification_model = YOLO(classification_model_checkpoint)
        self.class_names = ['bus', 'car', 'truck', 'two-wheeler']
        self.logger = logger
        self.visualise = visualise

    def optical_flow(self, frame, prev_frame=None):
        """
        Performs optical flow function on 2 concurrent images
        """
        # If no previous frame, use current frame to produce 0 values
        prev_frame = prev_frame if prev_frame is not None else frame
        
        # Convert current and prev frames to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

        # Calculate dense optical flow
        flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])

        return flow, mag, ang

    def process_optical_flow_output(self, flow, mag, ang):
        """
        Helper function to process optical flow outputs
        """
        average_speed = np.mean(mag),
        flow_variability = np.std(mag),
        traffic_density = np.sum(mag > 2.0) / mag.size * 100  # Percentage of moving pixels
        return average_speed[0].item(), flow_variability[0].item(), traffic_density.item()
    
    def process_yolo_output(self, frame, output, conf_thresh=0.0):
        """
        Helper function to process yolo model outputs
        """
        bboxes = []
        vehicle_counts = {'total':0}

        boxes = output[0].boxes
        if boxes is not None and len(boxes) > 0:
            for box in boxes:
                conf = float(box.conf[0])
                if conf > conf_thresh:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cls = self.class_names[int(box.cls[0])]
        
                    vehicle_counts['total'] += 1
                    vehicle_counts[cls] = vehicle_counts.get(cls, 0) + 1
                    bboxes.append([x1, y1, x2, y2])

        # Visualisation only if needed
        if self.visualise:
            self.display_congestion(frame, bboxes, vehicle_counts)

        return vehicle_counts, bboxes
    
    def process_classification_output(self, output, conf_thresh=0.0):
        """
        Helper function to process yolo model outputs
        """
        return

    async def run_processing(self, images={}):
        """
        Run async to detect vehicles in a time series of images using YOLOv11s model

        Args:
            Images [dict]: Dictionary of {camera_id: [data, data, data, ...], ...}
        
        Returns:
            Results [dict]: Dictionary of {camera_id: [{'total': 1, cls: 1, ...}, ...], ...}
        """
        if not images:
            self.logger.info('Error: No images passed into vehicle detector.')
            return

        self.logger.info('Running CV processing...')
        results = {}

        for camera_id, data in tqdm(images.items(), desc='Processing...'):
            results[camera_id] = []
            prev_frame = None

            for image_data in data:
                # Removing unnecessary image data metadata
                image_data.pop('location')
                frame = image_data.pop('image')
                timestamp = image_data.pop('timestamp')
                metadata = image_data.pop('metadata')

                # Re-formatting image data
                image_data['datetime'] = timestamp
                image_data['height'] = int(metadata['image_height'])
                image_data['width'] = int(metadata['image_width'])

                if frame is None:
                    self.logger.info(f'Error: Unable to load image for {camera_id}')
                    continue

                # Perform optical flow
                flow, mag, ang = self.optical_flow(frame, prev_frame)
                average_speed, flow_variability, traffic_density = self.process_optical_flow_output(flow, mag, ang)

                # Perform YOLOv11s object detection
                output = self.detection_model(frame, verbose=False)
                vehicle_counts, bboxes = self.process_yolo_output(frame, output)

                # Perform accident image classification
                # output = self.classification_model(frame)
                # self.process_classification_output(output)
                
                results[int(camera_id)].append({
                    'datetime': timestamp,
                    'pixel_speed': average_speed,
                    'flow_variability': flow_variability, 
                    'traffic_density': traffic_density,
                    'num_vehicles': vehicle_counts['total']
                })

                prev_frame = frame
                
        self.logger.info('Completed vehicle detection.')
        return images, results 
    
    def display_optical_flow(self, prev_frame, flow, mag, ang):
        """
        Displays optical flow output using cv2
        """
        # Prepare HSV image
        hsv = np.zeros_like(prev_frame)
        hsv[..., 1] = 255  # Set saturation to max for better visualization

        # Convert flow to HSV color representation
        mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        hsv[..., 0] = ang * 180 / np.pi / 2
        hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)

        # Convert HSV to BGR for visualization
        bgr_flow = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

        cv2.imshow("Optical Flow", bgr_flow)
        cv2.waitKey()
        cv2.destroyAllWindows()

    def display_congestion(self, frame, bboxes, vehicle_count):
        """
        Displays a singular frame with multiple bounding boxes using cv2
        """
        for bbox in bboxes:
            cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
        cv2.putText(frame, f"Vehicles: {vehicle_count['total']}", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow("Traffic Flow", frame)
        cv2.waitKey()
        cv2.destroyAllWindows()
