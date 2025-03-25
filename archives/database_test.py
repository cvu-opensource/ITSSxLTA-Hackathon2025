from Database import Database

def main():
    db = Database()

    # db.insert_cameras({
    #     '1000': {
    #         'lat': 1.0,
    #         'long': 2.0,
    #         'description': '1000'
    #     },
    #     '1001': {
    #         'lat': 3.0,
    #         'long': 4.0,
    #         'description': '1001'
    #     }
    # })
    # print(db.get_camera({'lta_camera_id': 1000}))
    # db.insert_images({
    #     '1000': [{
    #         'datetime': datetime.datetime(2025, 1, 2).isoformat(),
    #         'image_link': 'test4.com',
    #         'height': 1440,
    #         'width': 2560,
    #         'is_accident': True
    #     }],
    #     '1001': [{
    #         'datetime': datetime.datetime(2025, 3, 2).isoformat(),
    #         'image_link': 'test5.com',
    #         'height': 1440,
    #         'width': 2560,
    #         'is_accident': True
    #     }, {
    #         'datetime': datetime.datetime(2025, 3, 3).isoformat(),
    #         'image_link': 'test6.com',
    #         'height': 1440,
    #         'width': 2560,
    #         'is_accident': False
    #     }]
    # })
    # print(db.get_all_cameras())
    # print(db.get_image({'lta_camera_id': 1001}))
    # db.insert_traffic_flows({
    #     '1000': {
    #         "datetime": datetime.datetime(2025, 1, 21).isoformat(),
    #         "pixel_speed": 11234.5,
    #         "traffic_density": 55432.1,
    #         "num_vehicles": 888
    #     },
    #     '1001': {
    #         "datetime": datetime.datetime(2025, 1, 2).isoformat(),
    #         "pixel_speed": 66789.1,
    #         "traffic_density": 11987.6,
    #         "num_vehicles": 222
    #     }
    # })
    # print(db.get_traffic_flow_by_sensor_last_n({'lta_camera_id': 1001, 'n': 1}))

    # db.insert_images({'1001': [{'image_link': 'https://images.data.gov.sg/api/traffic-images/2025/03/ae231222-575f-4b4e-bffd-d80fbb9c2c1c.jpg', 'datetime': '2025-03-23T21:35:25+08:00', 'height': 240, 'width': 320, 'accident_detected': False}, {'image_link': 'https://images.data.gov.sg/api/traffic-images/2025/03/ae231222-575f-4b4e-bffd-d80fbb9c2c1c.jpg', 'datetime': '2025-03-23T21:35:25+08:00', 'height': 240, 'width': 320, 'accident_detected': False}]})
    # print(db.get_accidents_by_sensor_last_n({'lta_camera_id':1001, "n": 10}))

if __name__ == "__main__":
    main()