export const markers = {
  1001: {
    camera_data: {
        angle: 90,  // use this
        description: 'ECP (KPE) - Before KPE Exit',  // use this
        lat: 1.29531332,  // use this
        lng: 103.871146,  // use this
        accident_detected: false  // 'Accident detected' + turn red
    },
    traffic_data: {
        pixel_speed: {
            average: 0.5,  // 'Current pixel speed'
            relative: 0.2  // 'Relative pixel speed'
        },
        traffic_density: {
            average: 100.0,
            relative: 0.0  // 'Relative traffic density'
        },
        num_vehicles: {
            average: 2,  // 'Number of vehicles'
            relative: 0.02
        }
    },
  },
  1002: {
    camera_data: {
        angle: 270,  // use this
        description: 'PIE - From changi before KPE Exit',  // use this
        lat: 1.319541067,  // use this
        lng: 103.8785627,  // use this
        accident_detected: true  // 'Accident detected' + turn red
    },
    traffic_data: {
        pixel_speed: {
            average: 0.9,  // 'Current pixel speed'
            relative: 1.2  // 'Relative pixel speed'
        },
        traffic_density: {
            average: 200.0,
            relative: 2.3  // 'Relative traffic density'
        },
        num_vehicles: {
            average: 80,  // 'Number of vehicles'
            relative: 2.0
        }
    },
  },
  1003: {
    camera_data: {
        angle: 135,  // use this
        description: 'PIE - Towards Changi before KPE Exit',  // use this
        lat: 1.323957439,  // use this
        lng: 103.8728576,  // use this
        accident_detected: true  // 'Accident detected' + turn red
    },
    traffic_data: {
        pixel_speed: {
            average: 1.9,  // 'Current pixel speed'
            relative: 0.9  // 'Relative pixel speed'
        },
        traffic_density: {
            average: 167.0,
            relative: 1.1  // 'Relative traffic density'
        },
        num_vehicles: {
            average: 46,  // 'Number of vehicles'
            relative: 1.0
        }
    },
  },
};
