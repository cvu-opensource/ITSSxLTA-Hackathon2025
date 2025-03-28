# import requests
# import cv2
# import numpy as np

# url = "https://api.data.gov.sg/v1/transport/traffic-images"

# response = requests.get(url).json()

# acquisition_timestamp, cameras = response['items'][0]['timestamp'], response['items'][0]['cameras']
# print('acquisition timestamp', acquisition_timestamp)

# for idx, camera in enumerate(cameras):
#     print(camera['camera_id'], (camera['location']['latitude'], camera['location']['longitude']))
#     response = requests.get(camera['image'])

#     img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
#     img_array = np.frombuffer(response.content, np.uint8)
#     img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
#     cv2.imshow('img', img)
#     cv2.waitKey()

# cv2.destroyAllWindows



# import requests

# url = "https://api.data.gov.sg/v1/environment/rainfall"

# response = requests.get(url).json()

# readings = response['items'][0]['readings']
# readings = {station['station_id']:station['value'] for station in readings}

# stations = response['metadata']['stations']
# # print('stations', stations)
# stations = {
#     station['id']: {
#         'name': station['name'],
#         'location': (station['location']['latitude'], station['location']['longitude']),
#         'rainfall': readings[station['id']]
#     } for station in stations
# }
# # print('stations', stations)
# for idx, (id, station) in enumerate(stations.items()):
#     print(idx, id, station)


# from ultralytics import YOLO
# from pathlib import Path

# model = YOLO('../vehicle_detection.pt', imgsz=1000)
# files = list(Path('../images').rglob('*.jpg'))
# results = model(files)

# for result in results:
#     boxes = result.boxes  # Boxes object for bounding box outputs
#     masks = result.masks  # Masks object for segmentation masks outputs
#     keypoints = result.keypoints  # Keypoints object for pose outputs
#     probs = result.probs  # Probs object for classification outputs
#     obb = result.obb  # Oriented boxes object for OBB outputs
#     result.show()  # display to screen


# from ultralytics import YOLO
# from pathlib import Path

# model = YOLO('../vehicle_detection.pt')
# files = list(Path('../images').rglob('*.jpg'))
# results = model(files)

# for result in results:
#     img = cv2.imread(str(result.path)) # Load the image using opencv
#     boxes = result.boxes.xyxy.cpu().numpy().astype(int) # Get bounding box coordinates

#     for box in boxes:
#         x1, y1, x2, y2 = box
#         cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2) # Draw rectangle

#     cv2.imshow("Predictions", img)
#     cv2.waitKey(0) # show image until any key is pressed.
#     cv2.destroyAllWindows()



import cv2
import numpy as np
from pathlib import Path

def get_simulated_images():
    """Retrieves images from a folder, sorted by filename."""
    folder = Path("../data/DETRAC_Upload")
    image_paths = sorted(folder.rglob("*.jpg"))  # Sort ensures sequential processing
    return image_paths

def compute_optical_flow(image_paths):
    """Computes optical flow between sequential images using Farneback method."""
    if len(image_paths) < 2:
        print("Error: Not enough images to compute optical flow.")
        return

    # Load the first frame and convert to grayscale
    prev_frame = cv2.imread(str(image_paths[0]))
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    # Prepare HSV image
    hsv = np.zeros_like(prev_frame)
    hsv[..., 1] = 255  # Set saturation to max for better visualization

    for img_path in image_paths[1:]:  # Start from the second image
        frame = cv2.imread(str(img_path))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Calculate dense optical flow
        flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)

        # Convert flow to HSV color representation
        mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        hsv[..., 0] = ang * 180 / np.pi / 2
        hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)

        # Convert HSV to BGR for visualization
        bgr_flow = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        cv2.imshow("Optical Flow", bgr_flow)

        # Update previous frame
        prev_gray = gray.copy()

        # Exit on 'q' key press
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

# Run the optical flow computation on images
image_paths = get_simulated_images()
compute_optical_flow(image_paths)
