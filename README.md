#  Wind Power Forecasting API (Norway)

A production-ready **FastAPI-based wind forecasting system** that uses 20 years of ERA5-based wind farm data and an XGBoost model to predict real-time wind power at any given wind farm in Norway.

---

## 📦 What This Project Contains

- `main.py` – FastAPI app to serve wind power predictions
- `wind_power_xgb_model.pkl` – trained XGBoost model (based on 2.1.1)
- `requirements.txt` – Python dependencies


---

## 🔍 What We Did

### ✅ Data
- Used **ERA5** reanalysis wind speed data (u and v at 100m height, 0.25°*0.25° resolution)
- Collected 20 years of data (2003–2022) for all wind farms/Load centers in Norway
- Mapped daily wind speed to power output using a **2.1 MW rated Suzlon turbine power curve**
![image](https://github.com/user-attachments/assets/a5e09d6e-9385-4ab2-a0af-3a9be01ee29b)

### ✅ Model
- Trained an **XGBoost Regressor (v2.1.1)** using:
  - `lat`, `lon`, `wind_speed`, `day_of_year`
- Saved model using `joblib`
![image](https://github.com/user-attachments/assets/1e4a1dbc-fc89-4c1a-8598-7992cb041419)
![image](https://github.com/user-attachments/assets/fb7e68fa-ccf6-4342-987c-e84a3f7c269f)


### ✅ API Development
- Built with **FastAPI** + **Uvicorn**
- Input: lat, lon, date → auto-snapped to nearest ERA5 grid
- Uses **Open-Meteo** API to get real-time wind speed
- Applies XGBoost model to predict power output
- Cap power to 2.1 MW if wind speed ≥ 25 m/s(cut-out speed)

### ✅ Deployment Options
- Can be run with `uvicorn` manually
- Or started in background using `systemd` or `tmux`

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

- Grid resolution is 0.25°*0.25°→ inputs are snapped to nearest valid lat/lon
- Works only for Norway region (unless retrained)
- If wind speed ≥ 25 m/s → max output = 2.1 MW
- Model is trained assuming a single Suzlon turbine/site of 2.1 MW rating, therefore if installed capacity is more than that , simply multiply number of turbines needed to reach the capacity. For e.g. if at a site 10 MW capacity is installed , multiply the power output by (10/2.1)=4.76 , to get net power output at the site.   

---

## 🛠️ Future Improvements

- [ ] Add support for solar forecasting
- [ ] Country-wide generation dashboard
- [ ] DockerHub publishing
- [ ] CI/CD deployment

---

## 🧑‍💻 Author
Built by [Sandeep Sahu](https://github.com/itssahu) as part of a wind energy research project at IISc Bangalore.
