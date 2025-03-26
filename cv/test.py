import requests
import cv2
import numpy as np

# url = "https://api.data.gov.sg/v1/transport/traffic-images"

# response = requests.get(url).json()

# acquisition_timestamp, cameras = response['items'][0]['timestamp'], response['items'][0]['cameras']
# print('acquisition timestamp', acquisition_timestamp)

# for idx, camera in enumerate(cameras):
#     print(camera['camera_id'], (camera['location']['latitude'], camera['location']['longitude']))
#     # response = requests.get(camera['image'])

#     # img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
#     # img_array = np.frombuffer(response.content, np.uint8)
#     # img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
#     # cv2.imshow('img', img)
#     # cv2.waitKey()

# cv2.destroyAllWindows
# # print(response.json())

import requests

url = "https://api.data.gov.sg/v1/environment/rainfall"

response = requests.get(url).json()

readings = response['items'][0]['readings']
readings = {station['station_id']:station['value'] for station in readings}

stations = response['metadata']['stations']
# print('stations', stations)
stations = {
    station['id']: {
        'name': station['name'],
        'location': (station['location']['latitude'], station['location']['longitude']),
        'rainfall': readings[station['id']]
    } for station in stations
}
# print('stations', stations)
for idx, (id, station) in enumerate(stations.items()):
    print(idx, id, station)