# 🌬️ Wind Power Forecasting API (Norway)

A production-ready **FastAPI-based wind forecasting system** that uses 20 years of ERA5-based wind farm data and an XGBoost model to predict real-time wind power at any given coordinate in Norway.

---

## 📦 What This Project Contains

- `main.py` – FastAPI app to serve wind power predictions
- `wind_power_xgb_model.pkl` – trained XGBoost model (based on 2.1.1)
- `requirements.txt` – Python dependencies


---

## 🔍 What We Did

### ✅ Data
- Used **ERA5** reanalysis wind speed data (100m height, 0.25° resolution)
- Collected 20 years of data (2003–2022) for Norway
- Mapped rounded wind speed to power output using a **2.1 MW turbine power curve**

### ✅ Model
- Trained an **XGBoost Regressor (v2.1.1)** using:
  - `lat`, `lon`, `wind_speed`, `day_of_year`
- Saved model using `joblib`

### ✅ API Development
- Built with **FastAPI** + **Uvicorn**
- Input: lat, lon, date → auto-snapped to nearest ERA5 grid
- Uses **Open-Meteo** API to get real-time wind speed
- Applies XGBoost model to predict power output
- Cap power to 2.1 MW if wind speed ≥ 25 m/s

### ✅ Deployment Options
- Can be run with `uvicorn` manually
- Or started in background using `systemd` or `tmux`
- Optional: run with Docker (Dockerfile included)

---

## 🚀 How to Use

### 1. Clone the Repo
```bash
git clone https://github.com/<your-username>/wind-power-api.git
cd wind-power-api
```

### 2. Create & Activate Python Environment
```bash
conda create -n wind python=3.10 -y
conda activate wind
pip install -r requirements.txt
```

### 3. Run the API
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Open your browser:
```
http://localhost:8000/docs
```

You’ll see Swagger UI and can POST to `/forecast` with:
```json
{
  "lat": 60.12,
  "lon": 5.23,
  "date": "2025-04-14"
}
```

---

## 📌 Notes

- Grid resolution is 0.25° → inputs are snapped to nearest valid lat/lon
- Works only for Norway region (unless retrained)
- If wind speed ≥ 25 m/s → max output = 2.1 MW

---

## 🛠️ Future Improvements

- [ ] Add support for solar forecasting
- [ ] Country-wide generation dashboard
- [ ] DockerHub publishing
- [ ] CI/CD deployment

---

## 🧑‍💻 Author
Built by [Sandeep Sahu](https://github.com/itssahu) as part of a wind energy research project at IISc Bangalore.
