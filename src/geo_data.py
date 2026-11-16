"""
geo_data.py – SafeHer: Nationwide Geographical Data for India
Contains verified administrative hierarchy (28 States + 8 Union Territories),
district/city coordinates, localities, and state-level emergency helpline info.
"""

from typing import Dict, List, Tuple, Optional

# All 28 States and 8 Union Territories of India
STATES_AND_UTS = {
    # ── STATES ──
    "Andhra Pradesh": {
        "type": "State",
        "capital": "Amaravati",
        "helpline": "112 / 181 / 1091",
        "center": (15.9129, 79.7400),
        "cities": {
            "Visakhapatnam": {
                "center": (17.6868, 83.2185),
                "areas": ["Gajuwaka", "Madhurawada", "MVP Colony", "Dwaraka Nagar", "Rushikonda", "Siripuram"]
            },
            "Vijayawada": {
                "center": (16.5062, 80.6480),
                "areas": ["Benz Circle", "Governorpet", "Patamata", "Bhavanipuram", "Gandhinagar"]
            },
            "Guntur": {
                "center": (16.3067, 80.4365),
                "areas": ["Arundelpet", "Brodipet", "Kothapet", "Pattabhipuram", "Vidyanagar"]
            },
            "Tirupati": {
                "center": (13.6288, 79.4192),
                "areas": ["Alipiri", "Bhavani Nagar", "Chandragiri Road", "Korlagunta", "Renigunta"]
            },
            "Kurnool": {
                "center": (15.8281, 78.0373),
                "areas": ["Nandyal Checkpost", "Budhawara Peta", "B Camp", "Gayathri Estate"]
            }
        }
    },
    "Arunachal Pradesh": {
        "type": "State",
        "capital": "Itanagar",
        "helpline": "112 / 181",
        "center": (28.2180, 94.7278),
        "cities": {
            "Itanagar": {
                "center": (27.0844, 93.6053),
                "areas": ["Ganga Market", "Bank Tinali", "Naharlagun", "Niti Vihar", "Chimpu"]
            },
            "Tawang": {
                "center": (27.5861, 91.8594),
                "areas": ["Old Market", "Monastery Road", "Lhou", "Cona Area"]
            },
            "Pasighat": {
                "center": (28.0660, 95.3267),
                "areas": ["Main Bazaar", "Mirku", "Gumin Nagar", "Medical Colony"]
            }
        }
    },
    "Assam": {
        "type": "State",
        "capital": "Dispur",
        "helpline": "112 / 181 / 1091",
        "center": (26.2006, 92.9376),
        "cities": {
            "Guwahati": {
                "center": (26.1445, 91.7362),
                "areas": ["Paltan Bazaar", "Dispur", "Pan Bazaar", "GS Road", "Six Mile", "Jalukbari", "Beltola"]
            },
            "Silchar": {
                "center": (24.8333, 92.7789),
                "areas": ["Tarapur", "Rangirkhari", "Link Road", "Sadarghat"]
            },
            "Dibrugarh": {
                "center": (27.4728, 94.9120),
                "areas": ["Thana Chariali", "Amolapatty", "Jalan Nagar", "Graham Bazaar"]
            },
            "Jorhat": {
                "center": (26.7509, 94.2037),
                "areas": ["Gar-Ali", "Na-Ali", "Tarajan", "Choladhora"]
            }
        }
    },
    "Bihar": {
        "type": "State",
        "capital": "Patna",
        "helpline": "112 / 181",
        "center": (25.0961, 85.3131),
        "cities": {
            "Patna": {
                "center": (25.5941, 85.1376),
                "areas": ["Boring Road", "Kankarbagh", "Bailey Road", "Frazer Road", "Rajendra Nagar", "Danapur"]
            },
            "Gaya": {
                "center": (24.7914, 85.0002),
                "areas": ["Civil Lines", "Bodh Gaya Road", "AP Colony", "Rampur"]
            },
            "Muzaffarpur": {
                "center": (26.1209, 85.3647),
                "areas": ["Motijheel", "Mithanpura", "Brahmpura", "Aghoria Bazaar"]
            },
            "Bhagalpur": {
                "center": (25.2425, 86.9842),
                "areas": ["Tilka Manjhi", "Zero Mile", "Naya Bazaar", "Khanjarpur"]
            }
        }
    },
    "Chhattisgarh": {
        "type": "State",
        "capital": "Raipur",
        "helpline": "112 / 181",
        "center": (21.2787, 81.8661),
        "cities": {
            "Raipur": {
                "center": (21.2514, 81.6296),
                "areas": ["Pandri", "Telibandha", "Shankar Nagar", "Samta Colony", "Jaistambh Chowk"]
            },
            "Bhilai": {
                "center": (21.1938, 81.3509),
                "areas": ["Civic Centre", "Sector 6", "Nehru Nagar", "Supela"]
            },
            "Bilaspur": {
                "center": (22.0797, 82.1409),
                "areas": ["Vyapar Vihar", "Civil Lines", "Rajkishore Nagar", "Mangla"]
            }
        }
    },
    "Goa": {
        "type": "State",
        "capital": "Panaji",
        "helpline": "112 / 1091 / 181",
        "center": (15.2993, 74.1240),
        "cities": {
            "Panaji": {
                "center": (15.4909, 73.8278),
                "areas": ["Miramar", "Fontainhas", "Campal", "Dona Paula", "Patto Centre"]
            },
            "Margao": {
                "center": (15.2832, 73.9862),
                "areas": ["Comba", "Aquem", "Fatorda", "Gogol", "Pajifond"]
            },
            "Vasco da Gama": {
                "center": (15.3982, 73.8113),
                "areas": ["Chicalim", "Dabolim", "Baina", "Mormugao"]
            },
            "Mapusa": {
                "center": (15.5937, 73.8142),
                "areas": ["Market Area", "Feira Alta", "Angod", "Khorlim"]
            }
        }
    },
    "Gujarat": {
        "type": "State",
        "capital": "Gandhinagar",
        "helpline": "112 / 181 Abhayam",
        "center": (22.2587, 71.1924),
        "cities": {
            "Ahmedabad": {
                "center": (23.0225, 72.5714),
                "areas": ["Navrangpura", "SG Highway", "Vastrapur", "Maninagar", "Satellite", "Paldi", "Bopal"]
            },
            "Surat": {
                "center": (21.1702, 72.8311),
                "areas": ["Adajan", "Vesu", "Athwa", "Varachha", "Piplod", "Katargam"]
            },
            "Vadodara": {
                "center": (22.3072, 73.1812),
                "areas": ["Alkapuri", "Fatehgunj", "Manjalpur", "Sayajigunj", "Karelibaug"]
            },
            "Rajkot": {
                "center": (22.3039, 70.8022),
                "areas": ["Kalawad Road", "Yagnik Road", "University Road", "150 Feet Ring Road"]
            },
            "Gandhinagar": {
                "center": (23.2156, 72.6369),
                "areas": ["Sector 11", "Sector 21", "Infocity", "Kudasan", "Randesan"]
            }
        }
    },
    "Haryana": {
        "type": "State",
        "capital": "Chandigarh",
        "helpline": "112 / 1091 / 181",
        "center": (29.0588, 76.0856),
        "cities": {
            "Gurugram": {
                "center": (28.4595, 77.0266),
                "areas": ["Cyber City", "MG Road", "Sector 29", "Golf Course Road", "Sohna Road", "DLF Phase 3", "Udyog Vihar"]
            },
            "Faridabad": {
                "center": (28.4089, 77.3178),
                "areas": ["NIT Faridabad", "Sector 15", "Sector 16", "Greenfield", "Badkhal"]
            },
            "Panipat": {
                "center": (29.3909, 76.9635),
                "areas": ["Model Town", "GT Road Area", "Sector 11", "Sector 25"]
            },
            "Ambala": {
                "center": (30.3782, 76.7767),
                "areas": ["Ambala Cantt", "Ambala City", "Sector 7", "Model Town"]
            }
        }
    },
    "Himachal Pradesh": {
        "type": "State",
        "capital": "Shimla",
        "helpline": "112 / 181 Gudiya Helpline",
        "center": (31.1048, 77.1734),
        "cities": {
            "Shimla": {
                "center": (31.1048, 77.1734),
                "areas": ["Mall Road", "Sanjauli", "Chotta Shimla", "Summer Hill", "Lakkar Bazaar", "Kasumpti"]
            },
            "Dharamshala": {
                "center": (32.2190, 76.3234),
                "areas": ["Kotwali Bazaar", "McLeod Ganj", "Forsyth Ganj", "Dari"]
            },
            "Solan": {
                "center": (30.9045, 77.0967),
                "areas": ["Mall Road", "Chambaghat", "Saproon", "Deonghat"]
            },
            "Mandi": {
                "center": (31.7087, 76.9320),
                "areas": ["Indira Market", "Bhiuli", "Samkhetar", "Purani Mandi"]
            }
        }
    },
    "Jharkhand": {
        "type": "State",
        "capital": "Ranchi",
        "helpline": "112 / 181",
        "center": (23.6102, 85.2799),
        "cities": {
            "Ranchi": {
                "center": (23.3441, 85.3096),
                "areas": ["Main Road", "Lalpur", "Doranda", "Harmu", "Bariatu", "Kanke Road"]
            },
            "Jamshedpur": {
                "center": (22.8046, 86.2029),
                "areas": ["Bistupur", "Sakchi", "Kadma", "Sonari", "Telco"]
            },
            "Dhanbad": {
                "center": (23.7957, 86.4304),
                "areas": ["Bank More", "Hirapur", "Saraidhela", "Steel Gate"]
            }
        }
    },
    "Karnataka": {
        "type": "State",
        "capital": "Bengaluru",
        "helpline": "112 / 1091 / 181",
        "center": (15.3173, 75.7139),
        "cities": {
            "Bengaluru": {
                "center": (12.9716, 77.5946),
                "areas": ["Koramangala", "Indiranagar", "Whitefield", "Jayanagar", "Electronic City", "HSR Layout", "Malleshwaram", "Hebbal", "BTM Layout", "Marathahalli"]
            },
            "Mysuru": {
                "center": (12.2958, 76.6394),
                "areas": ["Gokulam", "Jayalakshmipuram", "Kuvempunagar", "Saraswathipuram", "Vijayanagar"]
            },
            "Mangaluru": {
                "center": (12.9141, 74.8560),
                "areas": ["Hampankatta", "Kadri", "Bejai", "Kankanady", "Surathkal"]
            },
            "Hubballi": {
                "center": (15.3647, 75.1240),
                "areas": ["Vidyanagar", "Keshwapur", "Gokul Road", "Shirur Park"]
            }
        }
    },
    "Kerala": {
        "type": "State",
        "capital": "Thiruvananthapuram",
        "helpline": "112 / 181 / 1091 Mithra",
        "center": (10.8505, 76.2711),
        "cities": {
            "Thiruvananthapuram": {
                "center": (8.5241, 76.9366),
                "areas": ["Kowdiar", "Pattom", "Palayam", "Vellayambalam", "Kazhakkoottam (Technopark)", "Thampanoor"]
            },
            "Kochi": {
                "center": (9.9312, 76.2673),
                "areas": ["MG Road", "Marine Drive", "Kakkanad (Infopark)", "Edappally", "Panampilly Nagar", "Fort Kochi"]
            },
            "Kozhikode": {
                "center": (11.2588, 75.7804),
                "areas": ["Mavoor Road", "Beach Road", "Nadakkavu", "Palayam", "Medical College Area"]
            },
            "Thrissur": {
                "center": (10.5276, 76.2144),
                "areas": ["Swaraj Round", "Ayyanthole", "Poothole", "Mannuthy"]
            }
        }
    },
    "Madhya Pradesh": {
        "type": "State",
        "capital": "Bhopal",
        "helpline": "112 / 1090 / 181",
        "center": (22.9734, 78.6569),
        "cities": {
            "Bhopal": {
                "center": (23.2599, 77.4126),
                "areas": ["MP Nagar", "Arera Colony", "Shahpura", "Kolar Road", "New Market", "Bittan Market"]
            },
            "Indore": {
                "center": (22.7196, 75.8577),
                "areas": ["Vijay Nagar", "Palasia", "MG Road", "Bhawarkua", "Rajwada", "AB Road"]
            },
            "Gwalior": {
                "center": (26.2183, 78.1828),
                "areas": ["City Centre", "Lashkar", "Morar", "Thatipur"]
            },
            "Jabalpur": {
                "center": (23.1815, 79.9864),
                "areas": ["Civil Lines", "Wright Town", "Napier Town", "Gorakhpur"]
            }
        }
    },
    "Maharashtra": {
        "type": "State",
        "capital": "Mumbai",
        "helpline": "112 / 1091 / 181",
        "center": (19.7515, 75.7139),
        "cities": {
            "Mumbai": {
                "center": (19.0760, 72.8777),
                "areas": ["Andheri", "Bandra", "Dadar", "Kurla", "Thane", "Borivali", "Malad", "Colaba", "Goregaon", "Powai"]
            },
            "Pune": {
                "center": (18.5204, 73.8567),
                "areas": ["Kothrud", "Viman Nagar", "Hinjawadi", "Baner", "Koregaon Park", "Shivajinagar", "Hadapsar", "Aundh"]
            },
            "Nagpur": {
                "center": (21.1458, 79.0882),
                "areas": ["Dharampeth", "Sitabuldi", "Ramdaspeth", "Sadar", "Civil Lines"]
            },
            "Thane": {
                "center": (19.2183, 72.9781),
                "areas": ["Naupada", "Ghodbunder Road", "Majiwada", "Vartak Nagar"]
            },
            "Nashik": {
                "center": (19.9975, 73.7898),
                "areas": ["College Road", "Gangapur Road", "Indira Nagar", "Panchavati"]
            },
            "Chhatrapati Sambhajinagar": {
                "center": (19.8762, 75.3433),
                "areas": ["Cidco", "Kranti Chowk", "Garkheda", "Samarth Nagar"]
            }
        }
    },
    "Manipur": {
        "type": "State",
        "capital": "Imphal",
        "helpline": "112 / 181",
        "center": (24.6637, 93.9063),
        "cities": {
            "Imphal": {
                "center": (24.8170, 93.9368),
                "areas": ["Thangal Bazaar", "Paona Bazaar", "Lamphelpat", "Uripok", "Singjamei"]
            },
            "Churachandpur": {
                "center": (24.3333, 93.6667),
                "areas": ["Tuibong", "New Bazaar", "Hiangtam Lamka", "Rengkai"]
            }
        }
    },
    "Meghalaya": {
        "type": "State",
        "capital": "Shillong",
        "helpline": "112 / 181",
        "center": (25.4670, 91.3662),
        "cities": {
            "Shillong": {
                "center": (25.5788, 91.8933),
                "areas": ["Police Bazaar", "Laitumkhrah", "Laband", "Mawkhar", "Nongthymmai"]
            },
            "Tura": {
                "center": (25.5141, 90.2023),
                "areas": ["Hawakhana", "Dobasipara", "Rongkhon", "Arapetta"]
            }
        }
    },
    "Mizoram": {
        "type": "State",
        "capital": "Aizawl",
        "helpline": "112 / 181",
        "center": (23.1645, 92.9376),
        "cities": {
            "Aizawl": {
                "center": (23.7271, 92.7176),
                "areas": ["Bara Bazaar", "Chanmari", "Zarkawt", "Khatla", "Bawngkawn"]
            },
            "Lunglei": {
                "center": (22.8878, 92.7369),
                "areas": ["Venglai", "Bazar Veng", "Rahsi Veng", "Chanmari-Lunglei"]
            }
        }
    },
    "Nagaland": {
        "type": "State",
        "capital": "Kohima",
        "helpline": "112 / 181",
        "center": (26.1584, 94.5624),
        "cities": {
            "Kohima": {
                "center": (25.6751, 94.1086),
                "areas": ["Main Town", "High School Colony", "PR Hill", "Razhoo Point", "BOC"]
            },
            "Dimapur": {
                "center": (25.9095, 93.7265),
                "areas": ["Circular Road", "Duncan Basti", "Purana Bazaar", "Burma Camp"]
            }
        }
    },
    "Odisha": {
        "type": "State",
        "capital": "Bhubaneswar",
        "helpline": "112 / 181 / 1091",
        "center": (20.9517, 85.0985),
        "cities": {
            "Bhubaneswar": {
                "center": (20.2961, 85.8245),
                "areas": ["Saheed Nagar", "Nayapalli", "Khandagiri", "Chandrasekharpur", "Patia (KIIT)", "Jayadev Vihar"]
            },
            "Cuttack": {
                "center": (20.4625, 85.8828),
                "areas": ["Badambadi", "Choudhury Bazaar", "CDA Sector", "Madhupatna"]
            },
            "Rourkela": {
                "center": (22.2604, 84.8536),
                "areas": ["Sector 19", "Uditnagar", "Civil Township", "Panposh"]
            }
        }
    },
    "Punjab": {
        "type": "State",
        "capital": "Chandigarh",
        "helpline": "112 / 181 Shakti",
        "center": (31.1471, 75.3412),
        "cities": {
            "Ludhiana": {
                "center": (30.9010, 75.8573),
                "areas": ["Model Town", "Sarabha Nagar", "Ferozepur Road", "Civil Lines", "BRS Nagar"]
            },
            "Amritsar": {
                "center": (31.6340, 74.8723),
                "areas": ["Mall Road", "Ranjit Avenue", "Civil Lines", "Lawrence Road", "Golden Temple Environs"]
            },
            "Jalandhar": {
                "center": (31.3260, 75.5762),
                "areas": ["Model Town", "Cantt Road", "Civil Lines", "Urban Estate"]
            },
            "Mohali": {
                "center": (30.7046, 76.7179),
                "areas": ["Phase 3B2", "Phase 7", "Sector 70", "Aerocity", "Phase 5"]
            }
        }
    },
    "Rajasthan": {
        "type": "State",
        "capital": "Jaipur",
        "helpline": "112 / 1090 / 181",
        "center": (27.0238, 74.2179),
        "cities": {
            "Jaipur": {
                "center": (26.9124, 75.7873),
                "areas": ["Malviya Nagar", "Vaishali Nagar", "C-Scheme", "Mansarovar", "Raja Park", "Tonk Road", "MI Road"]
            },
            "Jodhpur": {
                "center": (26.2389, 73.0243),
                "areas": ["Sardarpura", "Shastri Nagar", "Ratanada", "Paota"]
            },
            "Udaipur": {
                "center": (24.5854, 73.7125),
                "areas": ["Fateh Sagar Road", "Panchwati", "Hiran Magri", "Sukher"]
            },
            "Kota": {
                "center": (25.2138, 75.8648),
                "areas": ["Vigyan Nagar", "Talwandi", "Indra Vihar", "Dadabari"]
            }
        }
    },
    "Sikkim": {
        "type": "State",
        "capital": "Gangtok",
        "helpline": "112 / 181",
        "center": (27.5330, 88.5122),
        "cities": {
            "Gangtok": {
                "center": (27.3389, 88.6065),
                "areas": ["MG Marg", "Tadong", "Deorali", "Burtuk", "Sichey"]
            },
            "Namchi": {
                "center": (27.1667, 88.3500),
                "areas": ["Central Park", "Boomtar", "Maniram", "Damthang Road"]
            }
        }
    },
    "Tamil Nadu": {
        "type": "State",
        "capital": "Chennai",
        "helpline": "112 / 1091 / 181 Kavalan",
        "center": (11.1271, 78.6569),
        "cities": {
            "Chennai": {
                "center": (13.0827, 80.2707),
                "areas": ["T Nagar", "Anna Nagar", "Adyar", "Velachery", "OMR (IT Corridor)", "Mylapore", "Nungambakkam", "Besant Nagar"]
            },
            "Coimbatore": {
                "center": (11.0168, 76.9558),
                "areas": ["RS Puram", "Gandhipuram", "Peelamedu", "Saibaba Colony", "Saravanampatti"]
            },
            "Madurai": {
                "center": (9.9252, 78.1198),
                "areas": ["KK Nagar", "Anna Nagar", "Tallakulam", "Simmakkal"]
            },
            "Tiruchirappalli": {
                "center": (10.7905, 78.7047),
                "areas": ["Thillai Nagar", "Cantonment", "Srirangam", "KMC Area"]
            }
        }
    },
    "Telangana": {
        "type": "State",
        "capital": "Hyderabad",
        "helpline": "112 / 1091 / 181 Hawkeye",
        "center": (18.1124, 79.0193),
        "cities": {
            "Hyderabad": {
                "center": (17.3850, 78.4867),
                "areas": ["Banjara Hills", "Jubilee Hills", "HITEC City", "Gachibowli", "Madhapur", "Kukatpally", "Begumpet", "Secunderabad"]
            },
            "Warangal": {
                "center": (17.9689, 79.5941),
                "areas": ["Hanamkonda", "Kazipet", "Subedari", "Nakkalagutta"]
            },
            "Nizamabad": {
                "center": (18.6725, 78.0941),
                "areas": ["Khaleelwadi", "Subhashnagar", "Vinayaknagar", "Bodhan Road"]
            }
        }
    },
    "Tripura": {
        "type": "State",
        "capital": "Agartala",
        "helpline": "112 / 181",
        "center": (23.9408, 91.9882),
        "cities": {
            "Agartala": {
                "center": (23.8315, 91.2868),
                "areas": ["Banamalipur", "Radhanagar", "Battala", "Kunjaban", "Ramnagar"]
            },
            "Udaipur": {
                "center": (23.5333, 91.4833),
                "areas": ["Central Road", "Matabari", "Rajarbagh", "Fulbari"]
            }
        }
    },
    "Uttar Pradesh": {
        "type": "State",
        "capital": "Lucknow",
        "helpline": "112 / 1090 Women Powerline / 181",
        "center": (26.8467, 80.9462),
        "cities": {
            "Lucknow": {
                "center": (26.8467, 80.9462),
                "areas": ["Hazratganj", "Gomti Nagar", "Alambagh", "Indira Nagar", "Mahanagar", "Aliganj", "Vibhuti Khand"]
            },
            "Noida": {
                "center": (28.5355, 77.3910),
                "areas": ["Sector 18", "Sector 62", "Sector 15", "Sector 137", "Sector 76", "Noida Expressway"]
            },
            "Greater Noida": {
                "center": (28.4744, 77.5040),
                "areas": ["Alpha 1", "Beta 2", "Pari Chowk", "Knowledge Park III"]
            },
            "Kanpur": {
                "center": (26.4499, 80.3319),
                "areas": ["Civil Lines", "Kakadeo", "Swaroop Nagar", "Mall Road", "Govind Nagar"]
            },
            "Varanasi": {
                "center": (25.3176, 82.9739),
                "areas": ["Lanka (BHU)", "Sigra", "Godowlia", "Cantonment", "Bhelupur"]
            },
            "Agra": {
                "center": (27.1767, 78.0081),
                "areas": ["Tajganj", "Sanjay Place", "Civil Lines", "Dayalbagh", "Kamla Nagar"]
            },
            "Prayagraj": {
                "center": (25.4358, 81.8463),
                "areas": ["Civil Lines", "George Town", "Katrar", "Tagore Town", "Dhumanganj"]
            }
        }
    },
    "Uttarakhand": {
        "type": "State",
        "capital": "Dehradun",
        "helpline": "112 / 1090 / 181 Gaura Shakti",
        "center": (30.0668, 79.0193),
        "cities": {
            "Dehradun": {
                "center": (30.3165, 78.0322),
                "areas": ["Rajpur Road", "Paltan Bazaar", "Clement Town", "Ballupur", "Jakhan", "Vasant Vihar"]
            },
            "Haridwar": {
                "center": (29.9457, 78.1642),
                "areas": ["Har Ki Pauri", "Ranipur", "Jwalapur", "Kankhal", "Shivalik Nagar"]
            },
            "Rishikesh": {
                "center": (30.0869, 78.2676),
                "areas": ["Triveni Ghat", "Tapovan", "Muni Ki Reti", "Laxman Jhula Road"]
            },
            "Haldwani": {
                "center": (29.2183, 79.5130),
                "areas": ["Kaladhungi Road", "Nainital Road", "Kathgodam", "Mukhani"]
            }
        }
    },
    "West Bengal": {
        "type": "State",
        "capital": "Kolkata",
        "helpline": "112 / 1091 / 181",
        "center": (22.9868, 87.8550),
        "cities": {
            "Kolkata": {
                "center": (22.5726, 88.3639),
                "areas": ["Park Street", "Salt Lake (Bidhannagar)", "New Town", "Ballygunge", "Gariahat", "Howrah Environs", "Shyambazar", "Behala"]
            },
            "Howrah": {
                "center": (22.5958, 88.2636),
                "areas": ["Shibpur", "Salkia", "Mandirtala", "Bally"]
            },
            "Siliguri": {
                "center": (26.7271, 88.3953),
                "areas": ["Sevoke Road", "Pradhan Nagar", "Matigara", "Hakim Para"]
            },
            "Durgapur": {
                "center": (23.5204, 87.3119),
                "areas": ["City Centre", "Benachity", "Bidhannagar-Durgapur", "Steel Township"]
            }
        }
    },

    # ── UNION TERRITORIES ──
    "Andaman and Nicobar Islands": {
        "type": "Union Territory",
        "capital": "Port Blair",
        "helpline": "112 / 181",
        "center": (11.6234, 92.7265),
        "cities": {
            "Port Blair": {
                "center": (11.6234, 92.7265),
                "areas": ["Aberdeen Bazaar", "Haddo", "Garacharma", "Dollygunj", "School Line"]
            }
        }
    },
    "Chandigarh": {
        "type": "Union Territory",
        "capital": "Chandigarh",
        "helpline": "112 / 1091 / 181",
        "center": (30.7333, 76.7794),
        "cities": {
            "Chandigarh": {
                "center": (30.7333, 76.7794),
                "areas": ["Sector 17", "Sector 35", "Sector 22", "Sector 43", "Sector 26", "Manimajra", "Sector 8"]
            }
        }
    },
    "Dadra and Nagar Haveli and Daman and Diu": {
        "type": "Union Territory",
        "capital": "Daman",
        "helpline": "112 / 181",
        "center": (20.4283, 72.8397),
        "cities": {
            "Daman": {
                "center": (20.4283, 72.8397),
                "areas": ["Nani Daman", "Moti Daman", "Devka Beach Road", "Dunetha"]
            },
            "Silvassa": {
                "center": (20.2763, 73.0083),
                "areas": ["Kilvani Road", "Tokarkhada", "Samarvarni", "Amli"]
            }
        }
    },
    "Delhi": {
        "type": "Union Territory",
        "capital": "New Delhi",
        "helpline": "112 / 1091 / 181 Himmat",
        "center": (28.6139, 77.2090),
        "cities": {
            "Delhi": {
                "center": (28.6139, 77.2090),
                "areas": [
                    "Connaught Place", "Lajpat Nagar", "Saket", "Rohini",
                    "Dwarka", "Karol Bagh", "Nehru Place", "Chandni Chowk",
                    "Janakpuri", "Pitampura", "Hauz Khas", "Vasant Kunj"
                ]
            }
        }
    },
    "Jammu and Kashmir": {
        "type": "Union Territory",
        "capital": "Srinagar / Jammu",
        "helpline": "112 / 181 Sukoon",
        "center": (33.7782, 76.5762),
        "cities": {
            "Srinagar": {
                "center": (34.0837, 74.7973),
                "areas": ["Lal Chowk", "Rajbagh", "Karan Nagar", "Dalgate", "Hazratbal", "Hyderpora"]
            },
            "Jammu": {
                "center": (32.7266, 74.8570),
                "areas": ["Gandhi Nagar", "Trikuta Nagar", "Janipur", "Resham Ghar", "Bahu Fort Area"]
            }
        }
    },
    "Ladakh": {
        "type": "Union Territory",
        "capital": "Leh",
        "helpline": "112 / 181",
        "center": (34.1526, 77.5771),
        "cities": {
            "Leh": {
                "center": (34.1526, 77.5771),
                "areas": ["Main Bazaar", "Choglamsar", "Skara", "Sankar", "Changspa"]
            },
            "Kargil": {
                "center": (34.5539, 76.1349),
                "areas": ["Main Market", "Baroo", "Biamathang", "Poyen"]
            }
        }
    },
    "Lakshadweep": {
        "type": "Union Territory",
        "capital": "Kavaratti",
        "helpline": "112 / 181",
        "center": (10.5667, 72.6417),
        "cities": {
            "Kavaratti": {
                "center": (10.5667, 72.6417),
                "areas": ["Secretariat Area", "Ujra Mosque Environs", "Harbour Area", "South Beach"]
            }
        }
    },
    "Puducherry": {
        "type": "Union Territory",
        "capital": "Puducherry",
        "helpline": "112 / 1091 / 181",
        "center": (11.9416, 79.8083),
        "cities": {
            "Puducherry": {
                "center": (11.9416, 79.8083),
                "areas": ["White Town (French Quarter)", "Heritage Town", "Lawspet", "Muthialpet", "Nellithope"]
            },
            "Karaikal": {
                "center": (10.9254, 79.8380),
                "areas": ["Kamarajar Salai", "Beach Road", "Kottucherry", "Neravy"]
            }
        }
    }
}


def get_all_states() -> List[str]:
    """Return sorted list of all 28 states and 8 union territories."""
    return sorted(list(STATES_AND_UTS.keys()))


def get_states_by_type(entity_type: str = "State") -> List[str]:
    """Return list of entities matching 'State' or 'Union Territory'."""
    return sorted([k for k, v in STATES_AND_UTS.items() if v["type"] == entity_type])


def get_state_info(state_name: str) -> Optional[dict]:
    """Return info dict for a given state or UT."""
    return STATES_AND_UTS.get(state_name)


def get_cities_for_state(state_name: str) -> List[str]:
    """Return list of cities/districts available for a state."""
    state_info = STATES_AND_UTS.get(state_name)
    if not state_info:
        return []
    return sorted(list(state_info["cities"].keys()))


def get_areas_for_city(state_name: str, city_name: str) -> List[str]:
    """Return list of localities/areas for a specific city in a state."""
    state_info = STATES_AND_UTS.get(state_name)
    if not state_info:
        return []
    city_info = state_info["cities"].get(city_name)
    if not city_info:
        return []
    return sorted(city_info["areas"])


def get_location_coordinates(state_name: str, city_name: Optional[str] = None, area_name: Optional[str] = None) -> Tuple[float, float]:
    """
    Return (lat, lon) for the requested hierarchy level.
    Falls back gracefully from area -> city -> state -> national center.
    """
    state_info = STATES_AND_UTS.get(state_name)
    if not state_info:
        return (20.5937, 78.9629)  # Geographic center of India

    if not city_name or city_name not in state_info["cities"]:
        return state_info["center"]

    city_info = state_info["cities"][city_name]
    return city_info["center"]


def search_locations(query: str) -> List[dict]:
    """
    Search across States, UTs, Cities, and Localities.
    Returns matched items with hierarchy metadata and coordinates.
    """
    if not query or len(query.strip()) < 2:
        return []

    q = query.strip().lower()
    matches = []

    for state, sdata in STATES_AND_UTS.items():
        # Match state
        if q in state.lower():
            matches.append({
                "name": state,
                "type": sdata["type"],
                "state": state,
                "city": sdata["capital"],
                "coords": sdata["center"],
                "description": f"{sdata['type']} · Capital: {sdata['capital']}",
            })

        for city, cdata in sdata["cities"].items():
            if q in city.lower():
                matches.append({
                    "name": city,
                    "type": "District / City",
                    "state": state,
                    "city": city,
                    "coords": cdata["center"],
                    "description": f"City in {state}",
                })

            for area in cdata["areas"]:
                if q in area.lower():
                    matches.append({
                        "name": area,
                        "type": "Locality / Area",
                        "state": state,
                        "city": city,
                        "coords": cdata["center"],
                        "description": f"Locality in {city}, {state}",
                    })

    return matches[:15]
