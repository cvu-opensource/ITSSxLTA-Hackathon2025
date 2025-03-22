import requests
import cv2
import numpy as np

url = "https://api.data.gov.sg/v1/transport/traffic-images"

response = requests.get(url).json()

acquisition_timestamp, cameras = response['items'][0]['timestamp'], response['items'][0]['cameras']
print('acquisition timestamp', acquisition_timestamp)

for idx, camera in enumerate(cameras):
    print(idx, camera)
    response = requests.get(camera['image'])

    # img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
    img_array = np.frombuffer(response.content, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    print(img.shape)
    # cv2.imshow('img', img)
    # cv2.waitKey()

cv2.destroyAllWindows
# print(response.json())