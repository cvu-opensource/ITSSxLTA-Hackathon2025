"""
This script serves as hardcoded values PURELY for UI.
Involves certain camera details that do not come with the LTA API.
Keeping this out of the DB allows us to manipulate these values whenever necessary.
"""

camera_mapping = {
    'TPE': [1111, 1112, 1113, 7791, 7793, 7794, 7795, 7796, 7797, 7798],
    'CTE': [1701, 1702, 1703, 1704, 1705, 1706, 1707, 1709, 1711],
    'BKE': [2701, 2702, 2703, 2704, 2705, 2706, 2707, 2708],
    'ECP': [1001, 3702, 3704, 3705, 3793, 3795, 3796, 3797, 3798],
    'AYE': [4701, 4702, 4703, 4704, 4705, 4706, 4707, 4708, 4709, 4710, 4712, 4713, 4714, 4716],
    'PIEE': [5794, 5795, 5797, 5798, 5799],
    'PIEW': [6701, 6703, 6704, 6704, 6705, 6706, 6708, 6710, 6711, 6712, 6713, 6714, 6715, 6716],
    'KJE': [8701, 8702, 8704, 8706],
    'SLE': [9701, 9702, 9703, 9704, 9705, 9706],
    'PIE': [1002, 1003, 1004, 1004],
    'KPE': [1005, 1006],
    'MCE': [1501, 1502, 1503, 1504, 1505],
    'Sentosa': [4798, 4799]
}

camera_details = {
    1001: {
        'angle': 90,
        'description': 'ECP (KPE) - Before KPE Exit'
    },
    1002: {
        'angle': 270,
        'description': 'PIE - From changi before KPE Exit'
    },
    1003: {
        'angle': 135,
        'description': 'PIE - Towards Changi before KPE Exit'
    },
    1004: {
        'angle': 15,
        'description': 'PIE - Towards Tuas'
    },
    1005: {
        'angle': 30,
        'description': 'KPE - Towards ECP after Tampines Road'
    },
    1006: {
        'angle': 200,
        'description': 'KPE - Towards ECP near Defu Lane'
    },
    1111: {
        'angle': 95,
        'description': 'TPE(PIE) - Exit 2 to Loyang Ave'
    },
    1112: {
        'angle': 45,
        'description': 'TPE(PIE) - Tampines Viaduct'
    },
    1113: {
        'angle': 110,
        'description': 'Tanah Merah Coast Road towards Changi'
    },

    1501: {
        'angle': 290,
        'description': 'MCE - Towards ECP from Straits Blvd'
    },
    1502: {
        'angle': 45,
        'description': 'MCE - Entrance from Marina Coastal Drive'
    }, 
    1503: {
        'angle': 315,
        'description': 'MCE - Towards AYE at ERP 91'
    },
    1504: {
        'angle': 30,
        'description': 'MCE - Entrance from ECP'
    },
    1505: {
        'angle': 225,
        'description': 'MCE - Entrance from Marina Blvd'
    }, 

    1701: {
        'angle': 0,
        'description': 'CTE (AYE) - Moulmein Flyover LP448F'
    },
    1702: {
        'angle': 0,
        'description': 'CTE (AYE) - Braddell Flyover LP274F'
    },
    1703: {
        'angle': 0,
        'description': "CTE (SLE) - Blk 22 St George's Road"
    },
    1704: {
        'angle': 50,
        'description': 'CTE (AYE) - Entrance from Chin Swee Road'
    },
    1705: {
        'angle': 330,
        'description': 'CTE (AYE) - Ang Mo Kio Ave 5 Flyover '
    },
    1706: {
        'angle': 0,
        'description': 'CTE (AYE) - Yio Chu Kang Flyover '
    },
    1707: {
        'angle': 225,
        'description': 'CTE (AYE) - Bukit Merah Flyover '
    },
    1709: {
        'angle': 225,
        'description': 'CTE (AYE) - Exit 6 to Bukit Timah Road'
    },
    1711: {
        'angle': 180,
        'description': 'CTE (AYE) - Ang Mo Kio Flyover'
    },

    2701: {
        'angle': 315,
        'description': 'Woodlands Causeway (Towards Johor)'
    },
    2702: {
        'angle': 190,
        'description': 'Woodlands Checkpoint'
    },
    2703: {
        'angle': 330,
        'description': 'BKE (PIE) - Chantek F/O'
    },
    2704: {
        'angle': 325,
        'description': 'BKE (Woodlands Checkpoint) - Woodlands F/O'
    },
    2705: {
        'angle': 175,
        'description': 'BKE (PIE) - Dairy Farm F/O'
    },
    2706: {
        'angle': 0,
        'description': 'Entrance from Mandai Rd (Towards Checkpoint)'
    },
    2707: {
        'angle': 315,
        'description': 'Exit 5 to KJE (towards PIE)'
    },
    2708: {
        'angle': 350,
        'description': 'Exit 5 to KJE (Towards Checkpoint)'
    },

    3702: {
        'angle': 30,
        'description': 'ECP (Changi) - Entrance from PIE'
    },
    3704: {
        'angle': 225,
        'description': 'ECP (Changi) - Entrance from KPE'
    },
    3705: {
        'angle': 245,
        'description': 'ECP (AYE) - Exit 2A to Changi Coast Road'
    },

    3793: {
        'angle': 90,
        'description': 'ECP (Changi) - Laguna Flyover'
    },
    3795: {
        'angle': 55,
        'description': 'ECP (City) - Marine Parade F/O'
    },
    3796: {
        'angle': 55,
        'description': 'ECP (Changi) - Tanjong Katong F/O'
    },
    3797: {
        'angle': 315,
        'description': 'ECP (City) - Tanjung Rhu'
    },
    3798: {
        'angle': 30,
        'description': 'ECP (Changi) - Benjamin Sheares Bridge'
    },

    4701: {
        'angle': 135,
        'description': 'AYE (City) - Alexander Road Exit'
    },
    4702: {
        'angle': 305,
        'description': 'AYE (Jurong) - Keppel Viaduct'
    },
    4703: {
        'angle': 0,
        'description': 'Tuas Second Link'
    },
    4704: {
        'angle': 105,
        'description': 'AYE (CTE) - Lower Delta Road F/O'
    },
    4705: {
        'angle': 135,
        'description': 'AYE (MCE) - Entrance from Yuan Ching Rd'
    },
    4706: {
        'angle': 305,
        'description': 'AYE (Jurong) - NUS Sch of Computing TID'
    },
    4707: {
        'angle': 135,
        'description': 'AYE (MCE) - Entrance from Jln Ahmad Ibrahim'
    },
    4708: {
        'angle': 120,
        'description': 'AYE (CTE) - ITE College West Dover TID'
    },
    4709: {
        'angle': 270,
        'description': 'Clementi Ave 6 Entrance'
    },
    4710: {
        'angle': 285,
        'description': 'AYE(Tuas) - Pandan Garden'
    },
    4712: {
        'angle': 345,
        'description': 'AYE(Tuas) - Tuas Ave 8 Exit'
    },
    4713: {
        'angle': 135,
        'description': 'Tuas Checkpoint'
    },
    4714: {
        'angle': 315,
        'description': 'AYE (Tuas) - Near West Coast Walk'
    },
    4716: {
        'angle': 265,
        'description': 'AYE (Tuas) - Entrance from Benoi Rd'
    },

    4798: {
        'angle': 180,
        'description': 'Sentosa Tower 1'
    },
    4799: {
        'angle': 0,
        'description': 'Sentosa Tower 2'
    },

    5794: {
        'angle': 260,
        'description': 'PIEE (Jurong) - Bedok North'
    },
    5795: {
        'angle': 45,
        'description': 'PIEE (Jurong) - Eunos F/O'
    },
    5797: {
        'angle': 270,
        'description': 'PIEE (Jurong) - Paya Lebar F/O'
    },
    5798: {
        'angle': 270,
        'description': 'PIEE (Jurong) - Kallang Sims Drive Blk 62'
    },
    5799: {
        'angle': 225,
        'description': 'PIEE (Changi) - Woodsville F/O'
    },
    
    6701: {
        'angle': 75,
        'description': 'PIEW (Changi) - Blk 65A Jln Tenteram, Kim Keat'
    },
    6703: {
        'angle': 260,
        'description': 'PIEW (Changi) - Blk 173 Toa Payoh Lorong 1'
    },
    6704: {
        'angle': 285,
        'description': 'PIEW (Jurong) - Mt Pleasant F/O'
    },
    6705: {
        'angle': 250,
        'description': 'PIEW (Changi) - Adam F/O Special pole'
    },
    6706: {
        'angle': 120,
        'description': 'PIEW (Changi) - BKE'
    },
    6708: {
        'angle': 55,
        'description': 'Nanyang Flyover (Towards Changi)'
    },
    6710: {
        'angle': 195,
        'description': 'Entrance from Jln Anak Bukit (Towards Changi)'
    },
    6711: {
        'angle': 285,
        'description': 'Entrance from ECP (Towards Jurong)'
    },
    6712: {
        'angle': 270,
        'description': 'Exit 27 to Clementi Ave 6'
    },
    6713: {
        'angle': 225,
        'description': 'Entrance From Simei Ave (Towards Jurong)'
    },
    6714: {
        'angle': 0,
        'description': 'Exit 35 to KJE (Towards Changi)'
    },
    6715: {
        'angle': 290,
        'description': 'Hong Kah Flyover (Towards Jurong)'
    },
    6716: {
        'angle': 40,
        'description': 'AYE Flyover'
    },

    7791: {
        'angle': 325,
        'description': 'TPE (PIE) - Upper Changi F/O'
    },
    7793: {
        'angle': 270,
        'description': 'TPE(PIE) - Entrance to PIE from Tampines Ave 10'
    },
    7794: {
        'angle': 135,
        'description': 'TPE(SLE) - TPE Exit KPE'
    },
    7795: {
        'angle': 315,
        'description': 'TPE(PIE) - Entrance from Tampines FO'
    },
    7796: {
        'angle': 135,
        'description': 'TPE(SLE) - On rooflp of Blk 189A Rivervale Drive 9'
    },
    7797: {
        'angle': 80,
        'description': 'TPE(PIE) - Seletar Flyover'
    },
    7798: {
        'angle': 260,
        'description': 'TPE(SLE) - LP790F (On SLE Flyover)'
    },

    8701: {
        'angle': 45,
        'description': 'KJE (PIE) - Choa Chu Kang West Flyover'
    },
    8702: {
        'angle': 95,
        'description': 'KJE (BKE) - Exit To BKE'
    },
    8704: {
        'angle': 85,
        'description': 'KJE (BKE) - Entrance From Choa Chu Kang Dr'
    },
    8706: {
        'angle': 55,
        'description': 'KJE (BKE) - Tengah Flyover'
    },

    9701: {
        'angle': 85,
        'description': 'SLE (TPE) - Lentor F/O'
    },
    9702: {
        'angle': 135,
        'description': 'SLE(TPE) - Thomson Flyover'
    },
    9703: {
        'angle': 25,
        'description': 'SLE(Woodlands) - Woodlands South Flyover'
    },
    9704: {
        'angle': 75,
        'description': 'SLE(TPE) - Ulu Sembawang Flyover'
    },
    9705: {
        'angle': 270,
        'description': 'SLE(TPE) - Beside Slip Road From Woodland Ave 2'
    },
    9706: {
        'angle': 345,
        'description': 'SLE(Woodlands) - Mandai Lake Flyover'
    },
}