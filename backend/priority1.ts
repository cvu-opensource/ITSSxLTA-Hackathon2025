export const outlierTrafficData = {  // jic no traffic flow data - dyw to set some default value for the missing traffic data
    "TPE": {
        "priority": "Low",
        "average_rainfall": 0.0
    },
    "CTE": {"priority": "Low", "average_rainfall": 0.0},
    "BKE": {"priority": "Low", "average_rainfall": 0.0},
    "ECP": {"priority": "Low", "average_rainfall": 0.0},
    "AYE": {"priority": "Low", "average_rainfall": 0.0},
    "PIE": {"priority": "Low", "average_rainfall": 0.0},
    "KJE": {"priority": "Low", "average_rainfall": 0.0},
    "SLE": {"priority": "Low", "average_rainfall": 0.0},
    "KPE": {"priority": "Low", "average_rainfall": 0.0},
    "MCE": {"priority": "Low", "average_rainfall": 0.0},
    "Woodlands Checkpoint": {"priority": "Low", "average_rainfall": 0.0},
    "Tuas Checkpoint": {"priority": "Low", "average_rainfall": 0.0},
    "Sentosa": {"priority": "Low", "average_rainfall": 0.0},
}

export const TrafficData = {  // normal expected output - already ranked btw
    "Woodlands Checkpoint": {
        "pixel_speed": {"average_average": 0.0, "average_relative": 1.15},  // show relative 'Relative Pixel Speed'
        "traffic_density": {"average_average": 0.0, "average_relative": 0.0},  // show relative 'Relative Traffic Density' - but can dont show also cuz its scuffed af
        "num_vehicles": {"average_average": 22.11, "average_relative": 1.16},  // show average 'Average Vehicles Detected'
        "priority": "Normal",  // show 'Priority'
        "average_rainfall": 0.0,  // show 'Average Rainfall Detected (in mm)'
    },
    "Sentosa": {
        "pixel_speed": {"average_average": 0.0, "average_relative": 1.03},
        "traffic_density": {"average_average": 0.0, "average_relative": 0.0},
        "num_vehicles": {"average_average": 2.33, "average_relative": 1.23},
        "priority": "Normal",
        "average_rainfall": 0.0,
    },
    "Tuas Checkpoint": {
        "pixel_speed": {"average_average": 0.0, "average_relative": 1.05},
        "traffic_density": {"average_average": 0.0, "average_relative": 0.0},
        "num_vehicles": {"average_average": 7.17, "average_relative": 1.2},
        "priority": "Normal",
        "average_rainfall": 0.0,
    },
    "BKE": {
        "pixel_speed": {"average_average": 0.0, "average_relative": 0.96},
        "traffic_density": {"average_average": 0.0, "average_relative": 0.0},
        "num_vehicles": {"average_average": 9.67, "average_relative": 1.21},
        "priority": "Normal",
        "average_rainfall": 0.0,
    },
    "TPE": {
        "pixel_speed": {"average_average": 0.0, "average_relative": 1.03},
        "traffic_density": {"average_average": 0.0, "average_relative": 0.0},
        "num_vehicles": {"average_average": 6.83, "average_relative": 1.05},
        "priority": "Normal",
        "average_rainfall": 0.0,
    },
    "AYE": {
        "pixel_speed": {"average_average": 0.0, "average_relative": 1.01},
        "traffic_density": {"average_average": 0.0, "average_relative": 0.0},
        "num_vehicles": {"average_average": 4.56, "average_relative": 1.0},
        "priority": "Normal",
        "average_rainfall": 0.0,
    },
    "PIE": {
        "pixel_speed": {"average_average": 0.0, "average_relative": 1.04},
        "traffic_density": {"average_average": 0.0, "average_relative": 0.0},
        "num_vehicles": {"average_average": 7.04, "average_relative": 0.94},
        "priority": "Normal",
        "average_rainfall": 0.0,
    },
    "KJE": {
        "pixel_speed": {"average_average": 0.0, "average_relative": 1.0},
        "traffic_density": {"average_average": 0.0, "average_relative": 0.0},
        "num_vehicles": {"average_average": 4.33, "average_relative": 0.96},
        "priority": "Normal",
        "average_rainfall": 0.0,
    },
    "ECP": {
        "pixel_speed": {"average_average": 0.0, "average_relative": 1.06},
        "traffic_density": {"average_average": 0.0, "average_relative": 0.0},
        "num_vehicles": {"average_average": 5.37, "average_relative": 0.84},
        "priority": "Normal",
        "average_rainfall": 0.0,
    },
    "CTE": {
        "pixel_speed": {"average_average": 0.0, "average_relative": 0.97},
        "traffic_density": {"average_average": 0.0, "average_relative": 0.0},
        "num_vehicles": {"average_average": 10.48, "average_relative": 0.92},
        "priority": "Normal",
        "average_rainfall": 0.0,
    },
    "SLE": {
        "pixel_speed": {"average_average": 0.0, "average_relative": 1.0},
        "traffic_density": {"average_average": 0.0, "average_relative": 0.0},
        "num_vehicles": {"average_average": 9.67, "average_relative": 0.86},
        "priority": "Normal",
        "average_rainfall": 0.0,
    },
    "KPE": {
        "pixel_speed": {"average_average": 0.0, "average_relative": 0.94},
        "traffic_density": {"average_average": 0.0, "average_relative": 0.0},
        "num_vehicles": {"average_average": 2.83, "average_relative": 0.9},
        "priority": "Normal",
        "average_rainfall": 0.0,
    },
    "MCE": {
        "pixel_speed": {"average_average": 0.0, "average_relative": 1.03},
        "traffic_density": {"average_average": 0.0, "average_relative": 0.0},
        "num_vehicles": {"average_average": 0.2, "average_relative": 0.2},
        "priority": "Low",
        "average_rainfall": 0.0,
    },
}
