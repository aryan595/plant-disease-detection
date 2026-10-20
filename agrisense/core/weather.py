"""
AgriSense - Microclimate Weather & Disease Progression Engine
Integrates live weather for Pune / Maharashtra agricultural belts via Open-Meteo & OpenWeatherMap APIs.
Calculates real-time biological disease progression risks based on ambient humidity and temperature.
"""

import math
import os
import time
from typing import Dict, Optional, Tuple
import requests

# Coordinates for major Maharashtra agricultural belts (Default: Pune)
MAHARASHTRA_DISTRICTS = {
    "Pune (पुणे)": {"lat": 18.5204, "lon": 73.8567, "name_mr": "पुणे", "primary_crop": "Tomato / Vegetables"},
    "Nashik - Grape Belt (नाशिक - द्राक्ष पट्टा)": {"lat": 19.9975, "lon": 73.7898, "name_mr": "नाशिक", "primary_crop": "Grapes / Onion"},
    "Sangli - Tasgaon (सांगली - तासगाव)": {"lat": 16.8524, "lon": 74.5815, "name_mr": "सांगली", "primary_crop": "Grapes / Turmeric"},
    "Kolhapur - Soybean Belt (कोल्हापूर - सोयाबीन पट्टा)": {"lat": 16.7050, "lon": 74.2433, "name_mr": "कोल्हापूर", "primary_crop": "Soybean / Sugarcane"},
    "Narayangaon - Tomato Belt (नारायणगाव - टोमॅटो पट्टा)": {"lat": 19.1215, "lon": 73.9774, "name_mr": "नारायणगाव", "primary_crop": "Tomato"},
    "Solapur - Pomegranate Belt (सोलापूर - डाळिंब पट्टा)": {"lat": 17.6599, "lon": 75.9064, "name_mr": "सोलापूर", "primary_crop": "Pomegranate / Jowar"},
    "Ahmednagar - Rahuri MPKV (अहमदनगर - राहुरी)": {"lat": 19.3917, "lon": 74.6534, "name_mr": "अहमदनगर", "primary_crop": "Onion / Pomegranate"},
    "Satara - Strawberry & Soybean (सातारा - स्ट्रॉबेरी व सोयाबीन)": {"lat": 17.6805, "lon": 74.0183, "name_mr": "सातारा", "primary_crop": "Strawberry / Soybean"},
    "Nagpur - Orange Belt (नागपूर - संत्रा पट्टा)": {"lat": 21.1458, "lon": 79.0882, "name_mr": "नागपूर", "primary_crop": "Oranges / Cotton"},
    "Amravati - Cotton & Soybean (अमरावती - कापूस व सोयाबीन)": {"lat": 20.9320, "lon": 77.7523, "name_mr": "अमरावती", "primary_crop": "Soybean / Cotton"},
    "Jalgaon - Banana Belt (जळगाव - केळी पट्टा)": {"lat": 21.0077, "lon": 75.5626, "name_mr": "जळगाव", "primary_crop": "Banana / Cotton"},
    "Baramati - Sugarcane Belt (बारामती - ऊस पट्टा)": {"lat": 18.1517, "lon": 74.5772, "name_mr": "बारामती", "primary_crop": "Sugarcane / Soybean"},
    "Chhatrapati Sambhajinagar (छत्रपती संभाजीनगर)": {"lat": 19.8762, "lon": 75.3433, "name_mr": "संभाजीनगर", "primary_crop": "Cotton / Maize"},
}


def find_closest_district(lat: float, lon: float) -> Tuple[str, float]:
    """Finds the closest Maharashtra agricultural district using Haversine distance."""
    closest_key = "Pune (पुणे)"
    min_dist = float("inf")
    for key, info in MAHARASHTRA_DISTRICTS.items():
        dlat = math.radians(info["lat"] - lat)
        dlon = math.radians(info["lon"] - lon)
        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(math.radians(lat))
            * math.cos(math.radians(info["lat"]))
            * math.sin(dlon / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        dist_km = 6371.0 * c
        if dist_km < min_dist:
            min_dist = dist_km
            closest_key = key
    return closest_key, round(min_dist, 1)


def get_all_districts():
    """Returns structured list of supported Maharashtra agricultural districts."""
    return [
        {
            "id": k,
            "name": k,
            "name_mr": v["name_mr"],
            "primary_crop": v["primary_crop"],
            "lat": v["lat"],
            "lon": v["lon"]
        }
        for k, v in MAHARASHTRA_DISTRICTS.items()
    ]


_WEATHER_CACHE = {}
_CACHE_TTL_SECONDS = 300  # 5 minutes


def _localized_weather_fallback(
    district: str,
    district_mr: str,
    is_gps: bool,
    lat: float,
    lon: float,
    nearest_district: str,
    nearest_district_mr: str,
    distance_km: float,
) -> Dict:
    """Return a deterministic advisory baseline without a network dependency."""
    return {
        "source": "AgriSense Localized Meteorological Norms",
        "district": district,
        "district_mr": district_mr,
        "is_gps": is_gps,
        "lat": lat,
        "lon": lon,
        "nearest_district": nearest_district,
        "nearest_district_mr": nearest_district_mr,
        "distance_km": distance_km,
        "temperature_c": 27.5,
        "humidity_percent": 78,
        "wind_speed_kmh": 12.0,
        "description": "Humid / Cloudy",
        "success": False,
    }


def fetch_live_weather(
    district_key: str = "Pune (पुणे)",
    owm_api_key: Optional[str] = None,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    prefer_live: bool = True,
) -> Dict:
    """
    Fetch live ambient temperature, relative humidity, and precipitation with in-memory caching.
    Supports exact GPS coordinates (lat, lon) with automated nearest district matching.
    """
    now = time.time()
    is_gps = lat is not None and lon is not None
    location_key = f"gps_{round(lat, 3)}_{round(lon, 3)}" if is_gps else district_key
    # Analysis uses a fast advisory baseline; keep it separate from a cached
    # live observation returned by the dedicated weather route.
    cache_key = f"{location_key}|{'live' if prefer_live else 'analysis'}"

    if cache_key in _WEATHER_CACHE:
        cached_data, timestamp = _WEATHER_CACHE[cache_key]
        if now - timestamp < _CACHE_TTL_SECONDS:
            return cached_data

    if is_gps:
        closest_key, dist_km = find_closest_district(lat, lon)
        target_lat = lat
        target_lon = lon
        coords = MAHARASHTRA_DISTRICTS[closest_key]
        display_district = f"Live GPS ({lat:.3f}°N, {lon:.3f}°E)"
        display_district_mr = f"थेट जीपीएस ({lat:.3f}°N, {lon:.3f}°E)"
    else:
        coords = MAHARASHTRA_DISTRICTS.get(district_key, MAHARASHTRA_DISTRICTS["Pune (पुणे)"])
        target_lat = coords["lat"]
        target_lon = coords["lon"]
        closest_key = district_key
        dist_km = 0.0
        display_district = district_key
        display_district_mr = coords["name_mr"]

    fallback_res = _localized_weather_fallback(
        display_district,
        display_district_mr,
        is_gps,
        target_lat,
        target_lon,
        closest_key,
        coords["name_mr"],
        dist_km,
    )

    # Diagnosis must not wait behind a third-party weather provider. The
    # analysis endpoint deliberately uses this quick local advisory baseline;
    # the dedicated /weather route can still request live observations.
    if not prefer_live or os.getenv("ANALYSIS_WEATHER_MODE", "live").strip().lower() in {
        "offline",
        "local",
        "fallback",
    }:
        _WEATHER_CACHE[cache_key] = (fallback_res, now)
        return fallback_res

    # 1. Try OpenWeatherMap if key is available
    if owm_api_key or os.getenv("OPENWEATHERMAP_API_KEY"):
        key = owm_api_key or os.getenv("OPENWEATHERMAP_API_KEY")
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={target_lat}&lon={target_lon}&appid={key}&units=metric"
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                res = {
                    "source": "OpenWeatherMap",
                    "district": display_district,
                    "district_mr": display_district_mr,
                    "is_gps": is_gps,
                    "lat": target_lat,
                    "lon": target_lon,
                    "nearest_district": closest_key,
                    "nearest_district_mr": coords["name_mr"],
                    "distance_km": dist_km,
                    "temperature_c": round(data["main"]["temp"], 1),
                    "humidity_percent": int(data["main"]["humidity"]),
                    "wind_speed_kmh": round(data["wind"]["speed"] * 3.6, 1),
                    "description": data["weather"][0]["description"].title(),
                    "success": True
                }
                _WEATHER_CACHE[cache_key] = (res, now)
                return res
        except Exception:
            pass  # Seamlessly fall back to Open-Meteo

    # 2. Open-Meteo API (Free, high-precision, no rate limits, works for any lat/lon)
    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={target_lat}&longitude={target_lon}&current=temperature_2m,relative_humidity_2m,wind_speed_10m,precipitation"
        )
        resp = requests.get(url, timeout=6)
        if resp.status_code == 200:
            data = resp.json()["current"]
            temp = round(data["temperature_2m"], 1)
            humidity = int(data["relative_humidity_2m"])
            wind = round(data.get("wind_speed_10m", 0.0), 1)
            res = {
                "source": "Open-Meteo Live API",
                "district": display_district,
                "district_mr": display_district_mr,
                "is_gps": is_gps,
                "lat": target_lat,
                "lon": target_lon,
                "nearest_district": closest_key,
                "nearest_district_mr": coords["name_mr"],
                "distance_km": dist_km,
                "temperature_c": temp,
                "humidity_percent": humidity,
                "wind_speed_kmh": wind,
                "description": "Clear / Scattered Clouds" if humidity < 65 else "Humid / Overcast",
                "success": True
            }
            _WEATHER_CACHE[cache_key] = (res, now)
            return res
    except Exception as e:
        # Graceful historical typical fallback if network is offline
        print(f"[AgriSense] Weather API fallback ({e})")

    # Offline / Fail-safe Default
    _WEATHER_CACHE[cache_key] = (fallback_res, now)
    return fallback_res


def evaluate_progression_warning(
    disease_key: str,
    severity_level: str,
    humidity: int,
    temp_c: float,
    language: str = "en"
) -> Dict:
    """
    Biological epidemic progression warning based on ambient humidity and severity.
    Fungal spores (Downy Mildew, Rust, Blight) germinate aggressively when humidity > 75%.
    """
    is_healthy = "healthy" in disease_key.lower()

    if is_healthy:
        return {
            "risk_level": "Safe",
            "risk_level_mr": "सुरक्षित (Safe)",
            "banner_type": "success",
            "title_en": "Normal Canopy Conditions",
            "title_mr": "पिकाची स्थिती सुरक्षित आहे",
            "message_en": (
                f"Current temperature ({temp_c}°C) and humidity ({humidity}%) in Pune region "
                "pose no immediate threat to healthy foliage. Maintain standard cultural hygiene."
            ),
            "message_mr": (
                f"पुणे परिसरातील सध्याचे तापमान ({temp_c}°C) आणि आर्द्रता ({humidity}%) "
                "निरोगी पिकासाठी सामान्य आहे. कोणतीही आणीबाणी नाही."
            ),
            "action_en": "Routine scouting recommended in 5-7 days.",
            "action_mr": "५ ते ७ दिवसांनी नियमित पाहणी करा."
        }

    # High humidity conditions (> 75%)
    if humidity >= 75:
        if severity_level in ["Severe", "Moderate"]:
            return {
                "risk_level": "Critical",
                "risk_level_mr": "अतिधोकादायक (Critical Alert)",
                "banner_type": "error",
                "title_en": "🚨 HIGH EPIDEMIC PROGRESSION RISK",
                "title_mr": "🚨 रोगाचा वेगाने प्रसार होण्याची दाट शक्यता",
                "message_en": (
                    f"CRITICAL WARNING: Ambient humidity in Pune region is elevated at {humidity}% "
                    f"with temperature at {temp_c}°C. These microclimatic conditions accelerate fungal "
                    "spore germination and secondary mycelial proliferation within 24 to 48 hours. "
                    f"Combined with '{severity_level}' damage, rapid field-wide canopy scorching is imminent."
                ),
                "message_mr": (
                    f"गंभीर इशारा: सध्या हवेतील आर्द्रता {humidity}% असून तापमान {temp_c}°C आहे. "
                    "हे दमट हवामान बुरशीच्या बीजाणूंची संख्या अवघ्या २४ ते ४८ तासांत दुप्पट करू शकते. "
                    f"पिकावर आधीच '{severity_level}' प्रादुर्भाव असल्याने संपूर्ण शेतात रोग वेगाने पसरू शकतो."
                ),
                "action_en": "Immediate therapeutic fungicidal/bactericidal spray within 24 hours.",
                "action_mr": "पुढील २४ तासांच्या आत तात्काळ बुरशीनाशकाची फवारणी करा."
            }
        else:  # Mild with high humidity
            return {
                "risk_level": "Elevated",
                "risk_level_mr": "सावधानता इशारा (Elevated Risk)",
                "banner_type": "warning",
                "title_en": "⚠️ Weather Conducive to Disease Flare-up",
                "title_mr": "⚠️ हवामानामुळे रोग वाढण्याची शक्यता",
                "message_en": (
                    f"High ambient moisture ({humidity}%) creates a favorable nursery for pathogen spread. "
                    "While current damage is currently Mild, delayed action will trigger rapid escalation."
                ),
                "message_mr": (
                    f"हवेतील जास्त ओलावा ({humidity}%) रोगाच्या वाढीस पोषक आहे. "
                    "सध्या प्रादुर्भाव सौम्य असला तरी दुर्लक्ष केल्यास रोग वेगाने वाढेल."
                ),
                "action_en": "Apply preventative bio-fungicide or systemic barrier spray before rains.",
                "action_mr": "पाऊस सुरू होण्यापूर्वी प्रतिबंधात्मक सेंद्रिय किंवा बुरशीनाशक फवारणी करा."
            }

    # Moderate humidity (50% to 74%)
    elif 50 <= humidity < 75:
        return {
            "risk_level": "Moderate",
            "risk_level_mr": "मध्यम धोका (Moderate Risk)",
            "banner_type": "warning",
            "title_en": "Moderate Spread Velocity",
            "title_mr": "रोगाच्या प्रसाराचा मध्यम वेग",
            "message_en": (
                f"Moderate humidity ({humidity}%) and temperature ({temp_c}°C). Disease progress is steady. "
                "Early intervention will contain the infection to affected foliage."
            ),
            "message_mr": (
                f"मध्यम आर्द्रता ({humidity}%) आणि तापमान ({temp_c}°C). रोगाचा प्रसार स्थिर गतीने सुरू आहे. "
                "आताच फवारणी केल्यास रोग पुढील पानांवर जाणे रोखता येईल."
            ),
            "action_en": "Schedule chemical or organic spray during early morning or evening hours.",
            "action_mr": "सकाळी किंवा संध्याकाळी योग्य मात्रेनुसार फवारणीचे नियोजन करा."
        }

    # Dry weather (< 50%)
    else:
        return {
            "risk_level": "Low",
            "risk_level_mr": "कमी धोका (Low Spread)",
            "banner_type": "info",
            "title_en": "Dry Weather Inhibiting Fungal Sporulation",
            "title_mr": "कोरड्या हवेमुळे रोगाचा प्रसार मंदावला",
            "message_en": (
                f"Low ambient humidity ({humidity}%) naturally suppresses foliar spore sporulation. "
                "Existing necrotic spots will remain localized unless leaf wetness occurs."
            ),
            "message_mr": (
                f"कमी आर्द्रता ({humidity}%) असल्याने बुरशीचे बीजाणू तयार होणे मंदावले आहे. "
                "पाने कोरडी राहिल्यास रोग वेगाने पसरणार नाही."
            ),
            "action_en": "Prune visibly infected leaves and monitor for powdery mildew.",
            "action_mr": "रोगट पाने छाटून नष्ट करा आणि पावडरी मिल्ड्यूवर लक्ष ठेवा."
        }


def calculate_spray_window(
    temp_c: float,
    humidity: int,
    wind_speed_kmh: float,
    precipitation: float = 0.0
) -> Dict:
    """
    Computes agricultural spray feasibility based on CIBRC spray guidelines:
    - Wind: < 15 km/h is optimal (low drift risk). > 18 km/h causes dangerous chemical drift.
    - Temperature: 18°C - 32°C optimal. High noon heat (>34°C) causes rapid droplet evaporation and leaf scorching.
    - Humidity: 45% - 80% optimal. >85% + rain risk washes away expensive chemicals before absorption (rainfastness).
    """
    wind_safe = wind_speed_kmh <= 14.0
    wind_marginal = 14.0 < wind_speed_kmh <= 18.0
    rain_risk = precipitation > 0.2 or humidity >= 88

    if rain_risk or wind_speed_kmh > 18.0 or temp_c > 35.0:
        status = "AVOID"
        status_mr = "फवारणी टाळा (Avoid Spraying)"
        badge_color = "#ef4444"
        summary_en = "Current weather conditions pose high risk of chemical drift or rain wash-off."
        summary_mr = "सध्याच्या हवामानामुळे औषध वाहून जाण्याचा किंवा उडून वाया जाण्याचा धोका आहे."
    elif wind_marginal or temp_c > 32.0 or humidity > 80:
        status = "CAUTION"
        status_mr = "काळजीपूर्वक फवारणी करा (Caution)"
        badge_color = "#f59e0b"
        summary_en = "Marginal spray window. Use drift-reduction nozzles and a silicon spreader/sticker."
        summary_mr = "मध्यम परिस्थिती. फवारणी करताना स्टिकरचा (Spreader) वापर अवश्य करा."
    else:
        status = "OPTIMAL"
        status_mr = "फवारणीसाठी उत्तम वेळ (Safe to Spray)"
        badge_color = "#16a34a"
        summary_en = "Favorable microclimate. Low wind drift risk and good chemical absorption window."
        summary_mr = "हवामान अतिशय अनुकूल आहे. वारा कमी असल्याने औषध पानांवर व्यवस्थित बसेल."

    if wind_speed_kmh <= 12:
        wind_note_en = f"Calm to gentle breeze ({wind_speed_kmh} km/h) — Minimal spray drift"
        wind_note_mr = f"शांत वारा ({wind_speed_kmh} km/h) — औषध उडण्याचा धोका नाही"
    elif wind_speed_kmh <= 18:
        wind_note_en = f"Moderate breeze ({wind_speed_kmh} km/h) — Minor drift possible"
        wind_note_mr = f"मध्यम वारा ({wind_speed_kmh} km/h) — थोडा वारा आहे, सावधगिरी बाळगा"
    else:
        wind_note_en = f"Strong wind ({wind_speed_kmh} km/h) — High drift danger"
        wind_note_mr = f"वेगाने वाहणारा वारा ({wind_speed_kmh} km/h) — औषध हवेत उडून वाया जाईल"

    if humidity < 75 and precipitation == 0:
        rain_note_en = "Dry canopy expected (>4h rainfastness window)"
        rain_note_mr = "पुढील ४ तासांत पाऊस नाही, औषध पानांवर चांगले शोषले जाईल"
    else:
        rain_note_en = "Damp canopy; add rain-fast silicon sticker"
        rain_note_mr = "पानांवर ओलावा आहे; औषध धुतले जाऊ नये म्हणून स्टिकर मिसळा"

    return {
        "status": status,
        "status_mr": status_mr,
        "badge_color": badge_color,
        "summary_en": summary_en,
        "summary_mr": summary_mr,
        "best_hours_en": "Early Morning (6:30 AM – 9:30 AM) or Late Afternoon (4:30 PM – 6:30 PM)",
        "best_hours_mr": "सकाळी ६:३० ते ९:३० किंवा संध्याकाळी ४:३० ते ६:३०",
        "wind_note_en": wind_note_en,
        "wind_note_mr": wind_note_mr,
        "rain_note_en": rain_note_en,
        "rain_note_mr": rain_note_mr,
        "drift_risk_percent": min(int(wind_speed_kmh * 4), 95),
        "rain_wash_risk_percent": min(int(humidity * 0.7), 90) if humidity > 70 else 15
    }

