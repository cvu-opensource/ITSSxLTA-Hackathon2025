import requests

url = "https://api.data.gov.sg/v1/transport/traffic-images"

response = requests.get(url).json()

timestamp, cameras = response['items'][0]['timestamp'], response['items'][0]['cameras']
print('current timestamp', timestamp)

for idx, camera in enumerate(cameras):
    print(idx, camera)

# print(response.json())