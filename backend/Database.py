from supabase import create_client, Client
import datetime
import os
from dotenv import load_dotenv
load_dotenv()

class Database:
    def __init__(self):
        self.url = "https://ebirfqroikyfceiqeyhu.supabase.co"
        self.key = os.environ.get("SUPABASE_KEY")
        self.supabase = create_client(self.url, self.key)

    ## CAMERA

    def insert_cameras(self, dct):
        '''
        Function:   Inserts cameras into the database
        Input:      Dictionary with <lta_camera_id>: Dictionary with lat: float, long: float, description: string
        Output:     None
        '''
        for lta_camera_id, details in dct.items():
            self.supabase.rpc(
                'insert_camera', 
                params={
                    "lta_camera_id": lta_camera_id,
                    "lat": details['lat'], 
                    "long": details['long'], 
                    "description": details['description']
                }
            ).execute()

    def get_camera(self, dct):
        '''
        Function:   Gets camera details with lta_camera_id
        Input:      Dictionary with lta_camera_id: int
        Output:     Dictionary with lat: float, long: float, description: string
        '''
        response = self.supabase.rpc(
            'get_camera', 
            params={
                "lta_camera_id_in": dct['lta_camera_id']
            }
        ).execute()

        return response.data[0]
    
    def get_all_cameras(self):
        '''
        Function:   Gets all cameras
        Input:      None
        Output:     Dictionary with <lta_camera_id>: Dictionary with lat: float, long: float, description: string
        '''
        response = self.supabase.rpc('get_all_cameras').execute()
        temp = {}
        for i in response.data:
            temp[i['lta_camera_id']] = i
        return temp

    ## IMAGE
    
    def insert_images(self, dct):
        '''
        Function:   Inserts images into the database
        Input:      Dictionary with <camera_id>: List of Dictionary with datetime: string (in iso format), image_link: string, height: int, width: int
        Output:     None
        '''

        for lta_camera_id, lst in dct.items():
            for im in lst:
                self.supabase.rpc(
                    'insert_image', 
                    params={
                        "lta_camera_id_in": lta_camera_id,
                        "datetime": im['datetime'],
                        "image_link": im['image_link'],
                        "height": im['height'],
                        "width": im['width'],
                        "accident_detected": im['accident_detected']
                    }
                ).execute()

    def get_image(self, dct):
        '''
        Function:   Gets most recent image for camera from the database
        Input:      Dictionary with lta_camera_id: int
        Output:     Dictionary with datetime: string (in iso format), image_link: string, height: int, width: int
        '''
        response = self.supabase.rpc(
            'get_image', 
            params={
                "lta_camera_id_in": dct['lta_camera_id']
            }
        ).execute()

        return response.data[0]
    
    ## TRAFFIC FLOW

    def insert_traffic_flows(self, dct):
        '''
        Function:   Inserts traffic flows into the database
        Input:      Dictionary with <camera_id>: Dictionary with datetime: string (in iso format), pixel_speed: float, traffic_density: float, num_vehicles: int
        Output:     None
        '''

        for lta_camera_id, details in dct.items():
            self.supabase.rpc(
                'insert_traffic_flow', 
                params={
                    "lta_camera_id_in": lta_camera_id,
                    "datetime": details['datetime'],
                    "pixel_speed": details['pixel_speed'],
                    "traffic_density": details['traffic_density'],
                    "num_vehicles": details['num_vehicles']
                }
            ).execute()
    
    def get_traffic_flow_by_sensor_last_n(self, dct):
        '''
        Function:   Gets last n records of traffic flow by sensor
        Input:      Dictionary with lta_camera_id: int, n: int
        Output:     Dictionary with <datetime string>: Dictionary with pixel_speed: float, traffic_density: float, num_vehicles: int
        '''

        response = self.supabase.rpc(
            'get_traffic_flow', 
            params={
                "lta_camera_id_in": dct['lta_camera_id']
            }
        ).execute()

        temp = {}
        for i in response.data[:dct['n']]:
            temp[i['datetime']] = i
        return temp