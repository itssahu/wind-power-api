from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import joblib
import numpy as np
import requests

# Load model
model = joblib.load("/vol/sandeep_storage/Files2/wind_api/wind_power_xgb_model.pkl")

app = FastAPI(title="Wind Power Forecasting API")

# Request schema
class ForecastRequest(BaseModel):
    lat: float
    lon: float
    date: str  # Format: "YYYY-MM-DD"

# Snap coordinates to ERA5 grid
def snap_to_grid(lat, lon, res=0.25):
    return round(lat / res) * res, round(lon / res) * res

# Fetch wind speed from Open-Meteo
def get_wind_speed(lat, lon, date):
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&hourly=wind_speed_100m"
        f"&timezone=auto&start_date={date}&end_date={date}"
    )
    try:
        r = requests.get(url)
        data = r.json()
        wind_speed = data["hourly"]["wind_speed_100m"][12]  # noon value
        return wind_speed
    except Exception as e:
        print(f"Error fetching wind speed: {e}")
        return None

@app.post("/forecast")
def forecast(req: ForecastRequest):
    lat_snap, lon_snap = snap_to_grid(req.lat, req.lon)
    wind_speed = get_wind_speed(lat_snap, lon_snap, req.date)

    if wind_speed is None:
        return {"error": "Wind speed data not available"}

    day_of_year = datetime.strptime(req.date, "%Y-%m-%d").timetuple().tm_yday

    # Apply turbine power logic
    if wind_speed < 3.5:
        predicted_power = 0.0
    elif wind_speed >= 25.0:
        predicted_power = 2.1
    else:
        X = np.array([[lat_snap, lon_snap, wind_speed, day_of_year]])
        predicted_power = model.predict(X)[0]

    return {
        "input": {
            "requested_lat": req.lat,
            "requested_lon": req.lon,
            "date": req.date
        },
        "snapped_to_grid": {
            "lat": lat_snap,
            "lon": lon_snap
        },
        "wind_speed_100m": round(wind_speed, 2),
        "predicted_power_MW": round(predicted_power, 3)
    }
