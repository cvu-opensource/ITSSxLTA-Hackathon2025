import cv2
import asyncio
from ultralytics import YOLO
from tqdm import tqdm


class VehicleDetector:
    def __init__(self, model_checkpoint, logger, visualise=False):
        if not model_checkpoint:
            raise ValueError("Error: VEHICLE_DETECTION_CKPT is not set in the environment variables.")
        
        self.model = YOLO(model_checkpoint, verbose=False)
        self.class_names = ['bus', 'car', 'truck', 'two-wheeler']
        self.logger = logger
        self.visualise = visualise

    async def detect_vehicles(self, images={}):
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

        self.logger.info('Running vehicle detection...')
        results = {}
        for camera_id, data in tqdm(images.items(), desc='Processing...'):
            results[camera_id] = []
            for image_data in data:
                frame = image_data['image']
                if frame is None:
                    print(f"Error: Unable to load image for {camera_id}")
                    continue
                
                # Perform YOLOv11s object detection
                output = self.model(frame, verbose=False)
                boxes = output[0].boxes
                
                # Extract detected vehicles
                bboxes = []
                vehicle_counts = {
                    'total':0
                }

                if boxes is not None and len(boxes) > 0:
                    for box in boxes:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        conf = float(box.conf[0])
                        cls = self.class_names[int(box.cls[0])]

                        vehicle_counts['total'] += 1
                        vehicle_counts[cls] = vehicle_counts.get(cls, 0) + 1
                        bboxes.append([x1, y1, x2, y2])

                # Visualisation only if needed
                if self.visualise:
                    self.display_congestion(frame, bboxes, vehicle_counts)

                results[camera_id].append(sorted(vehicle_counts))
                
        self.logger.info('Completed vehicle detection.')
        print('results', results)
        return results 

    def display_congestion(self, frame, bboxes, vehicle_count):
        """
        Displays a singular frame with multiple bounding boxes using cv2
        """
        for bbox in bboxes:
            cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[3], bbox[4]), (0, 255, 0), 2)
        cv2.putText(frame, f"Vehicles: {vehicle_count['total']}", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow("Traffic Flow", frame)
        cv2.waitKey()
        cv2.destroyAllWindows()
