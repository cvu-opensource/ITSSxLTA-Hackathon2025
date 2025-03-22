from ultralytics import YOLO


class AccidentDetector:
    def __init__(self, model_checkpoint, logger):
        if not model_checkpoint:
            raise ValueError("Error: ACCIDENT_DETECTION_CKPT is not set in the environment variables.")

        self.model = YOLO(model_checkpoint, verbose=False)
        self.logger = logger

    async def detect_accident(self, images):
        """
        Given a series of frames, run transformer to detect if and when an accident occured
        
        Args:
            Images [dict]: Dictionary of {camera_id: [data, data, data, ...], ...}
        
        Returns:
            Results [dict]: Dictionary of {camera_id: [], ...}
            """
        if not images:
            self.logger.info('Error: No images passed into accident detector.')
            return

        self.logger.info('Running accident detection...')
        results = {}
        for camera_id, data in images.items():
            compiled_images = [
                item['image'] for item in data
            ]

            # TODO: Feed compiled_images into ben's model

            # TODO: Process outputs into results

        self.logger.info('Completed accident detection.')
        return results