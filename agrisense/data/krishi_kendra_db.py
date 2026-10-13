"""
AgriSense - Maharashtra Krishi Seva Kendra & CIB&RC Benchmark Directory
Verified agro-input dealers, IFFCO Kisan Kendras, and standard MRP price ranges
to protect farmers from counterfeit products and dealer price gouging.
"""

from typing import Dict, List, Any

# Benchmark retail price guide for popular agrochemical formulations (CIB&RC approved)
FORMULATION_PRICING_GUIDE = [
    {"formulation": "Mancozeb 75% WP", "pack_size": "500 gm", "fair_mrp_inr": "₹320 - ₹380", "popular_brands": "Dithane M-45, Indofil M-45, UPL Saaf (Mix)"},
    {"formulation": "Metalaxyl 8% + Mancozeb 64% WP", "pack_size": "500 gm", "fair_mrp_inr": "₹550 - ₹680", "popular_brands": "Ridomil Gold, Krilaxyl"},
    {"formulation": "Chlorothalonil 75% WP", "pack_size": "500 gm", "fair_mrp_inr": "₹450 - ₹550", "popular_brands": "Kavach (Syngenta), Ishan"},
    {"formulation": "Copper Oxychloride 50% WP", "pack_size": "500 gm", "fair_mrp_inr": "₹340 - ₹420", "popular_brands": "Blitox 50, Blue Copper"},
    {"formulation": "Hexaconazole 5% SC", "pack_size": "1 Litre", "fair_mrp_inr": "₹480 - ₹600", "popular_brands": "Contaf Plus, Sitara"},
    {"formulation": "Azoxystrobin 23% SC", "pack_size": "200 ml", "fair_mrp_inr": "₹750 - ₹920", "popular_brands": "Amistar, Godrej Mirador"},
    {"formulation": "Neem Oil 10,000 PPM", "pack_size": "1 Litre", "fair_mrp_inr": "₹450 - ₹580", "popular_brands": "Nimbecidine, Econeem"}
]

# Registered Krishi Seva Kendra hubs per Maharashtra agricultural belt
KRISHI_KENDRA_DIRECTORY = {
    "Pune (पुणे)": [
        {"name": "Shivkrupa Krishi Seva Kendra", "address": "Market Yard, Gultekdi, Pune", "phone": "020-24261890", "type": "Authorized Dealer (Bayer/Syngenta)"},
        {"name": "IFFCO Kisan Seva Kendra", "address": "Hadapsar APMC Sub-Yard, Pune", "phone": "1800-103-1967", "type": "Government Cooperative"},
        {"name": "Balaji Agro Agencies", "address": "Manchar Road, Ambegaon / Narayangaon", "phone": "02133-223450", "type": "Pesticide & Drip Hub"}
    ],
    "Nashik - Grape Belt (नाशिक - द्राक्ष पट्टा)": [
        {"name": "Pimpalgaon Grape Agro Center", "address": "Near APMC Market, Pimpalgaon Baswant", "phone": "02550-251234", "type": "Grape Export Advisory & Inputs"},
        {"name": "Sahyadri Agro Store", "address": "Mohadi, Dindori Road, Nashik", "phone": "0253-2394000", "type": "Farmer Producer Co. (Sahyadri)"},
        {"name": "Kisan Krishi Seva Kendra", "address": "CBS Bus Stand, Nashik City", "phone": "0253-2578912", "type": "Certified Input Hub"}
    ],
    "Sangli - Tasgaon (सांगली - तासगाव)": [
        {"name": "Tasgaon Bedana & Krishi Seva", "address": "Station Road, Tasgaon, Sangli", "phone": "02346-240150", "type": "Grape & Raisin Specialist"},
        {"name": "Sangli Jilha Krishi Vikas Kendra", "address": "Market Yard, Sangli", "phone": "0233-2671200", "type": "IFFCO / RCF Fertilizer Hub"}
    ],
    "Kolhapur - Soybean Belt (कोल्हापूर - सोयाबीन पट्टा)": [
        {"name": "Shree Mahalaxmi Agro Agency", "address": "Shahupuri, Kolhapur", "phone": "0231-2654321", "type": "Soybean Seed & Protection Hub"},
        {"name": "Kagal Taluka Shetkari Sangh", "address": "Kagal, Kolhapur", "phone": "02325-244100", "type": "Cooperative Store"}
    ],
    "Narayangaon - Tomato Belt (नारायणगाव - टोमॅटो पट्टा)": [
        {"name": "Tomato Valley Agro Services", "address": "Pune-Nashik Highway, Narayangaon", "phone": "02132-242180", "type": "Tomato Nursery & Crop Care"},
        {"name": "Vighnaharta Krishi Kendra", "address": "Near ST Stand, Junnar", "phone": "02132-222390", "type": "Vegetable Specialist"}
    ]
}

def get_krishi_kendras_for_district(district_key: str) -> Dict[str, Any]:
    """Returns local registered Krishi Seva Kendras and fair price benchmarks."""
    kendras = KRISHI_KENDRA_DIRECTORY.get(district_key, KRISHI_KENDRA_DIRECTORY["Pune (पुणे)"])
    return {
        "district": district_key,
        "kendras": kendras,
        "pricing_guide": FORMULATION_PRICING_GUIDE
    }
