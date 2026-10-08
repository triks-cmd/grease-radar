# Grease Radar — Hack4Vilnius Challenge 12

**Prevent wastewater blockages before they happen.**

Grease Radar is a preventive monitoring system that identifies recurring wastewater blockage hotspots and helps cities prioritize preventive inspection using transparent, explainable risk scoring.

## 🎯 Challenge

Challenge 12: Preventing sewer system blockages and reducing grease/contaminants entering wastewater.

## 💡 Solution

Instead of reacting to blockages after they occur, Grease Radar:
- Analyzes historical incident data
- Identifies high-risk hotspot areas
- Calculates transparent risk scores
- Enables data-driven preventive maintenance

## ✨ Features

### Core Functionality
- **Interactive Map**: Visualize all historical incidents and risk hotspots on a Vilnius map
- **Hotspot Detection**: Automatic identification of recurring problem areas using spatial grid analysis
- **Transparent Risk Score**: Explainable 0-100 risk score based on four factors:
  - Frequency (35%): number of incidents
  - Recurrence (30%): distinct months with incidents
  - Recency (20%): how recently incidents occurred
  - Spatial Density (15%): nearby incident cells
- **Risk Breakdown**: Detailed explanation of why each hotspot received its score
- **Priority List**: Ranked list of hotspots for systematic inspection
- **Historical Backtesting**: Validation on historical data (70-30 train-test split)
- **CSV Import**: Easy integration with official Vilniaus vandenys data

### UI/UX
- Professional municipal monitoring tool design
- Color-coded risk levels (HIGH/MEDIUM/LOW)
- Interactive map with click-to-inspect
- Responsive layout for different screen sizes
- Clear visual hierarchy and information architecture

## 🚀 Quick Start

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate
# Activate (macOS/Linux)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Open http://127.0.0.1:5000 in your browser.

## 📊 Data Format

The system accepts CSV files with the following required columns:
- **latitude** (or lat, y): Incident latitude
- **longitude** (or lon, lng, longitude, x): Incident longitude
- **date** (or datetime, incident_date, data): Incident date

Additional columns are allowed and ignored. The system filters to Vilnius coordinates (54.5-54.9°N, 25.0-25.6°E).

### Official Data
Place the official Vilniaus vandenys incident CSV at `data/incidents.csv`, or use the Import button in the UI.

### Demo Data
The included `data/demo_incidents.csv` is synthetic data for demonstration purposes only. **Do not present demo data as official results.**

## 🧮 Technical Details

### Risk Score Calculation

For each spatial grid cell (~500m):

1. **Frequency**: Number of incidents in the cell, normalized 0-100
2. **Recurrence**: Number of distinct months with incidents, normalized 0-100
3. **Recency**: Exponential decay based on days since last incident: `100 * exp(-days/180)`
4. **Spatial Density**: Count of occupied neighboring cells (3x3 grid), normalized 0-100

Overall Risk Score:
```
Risk = 0.35 * Frequency + 0.30 * Recurrence + 0.20 * Recency + 0.15 * Density
```

Risk Levels:
- HIGH: Risk ≥ 70
- MEDIUM: Risk ≥ 40
- LOW: Risk < 40

### Backtesting Methodology

1. Sort incidents by date
2. Split at 70% temporal cutoff
3. Train model on earlier incidents
4. Identify top 20% risk cells from training
5. Test: measure how many future incidents fall in those cells
6. Report capture rate and statistics

### Architecture

**Backend**
- Flask web framework
- Pandas for data processing
- NumPy for numerical calculations
- Spatial grid-based aggregation

**Frontend**
- Leaflet.js for interactive mapping
- Vanilla JavaScript (no framework overhead)
- Custom CSS with modern design system

**Data Pipeline**
1. CSV import and validation
2. Coordinate filtering (Vilnius bounds)
3. Spatial grid assignment
4. Metric calculation and normalization
5. Risk score computation
6. Hotspot ranking
7. Backtesting validation
8. JSON API response

## 📁 Project Structure

```
grease_radar_mvp/
├── app.py                 # Flask application and core logic
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── DEMO_SCENARIO.md      # Demo script and talking points
├── data/
│   ├── demo_incidents.csv  # Synthetic demo data
│   └── incidents.csv       # Official data (add here)
├── static/
│   ├── app.js            # Frontend JavaScript
│   └── style.css         # Custom styling
└── templates/
    └── index.html        # Main HTML template
```

## 🎨 Design Principles

1. **Transparency**: No black-box AI - all risk factors are explainable
2. **Validation**: Backtested on historical data before claims
3. **Practicality**: Built for municipal workflows, not research
4. **Focus**: Single clear use case, not trying to do everything
5. **Professional**: UI looks like a real municipal tool, not a student project

## 📋 Demo Checklist

Before presenting:
- [ ] Server running successfully
- [ ] Map loads with OpenStreetMap tiles
- [ ] All hotspots display correctly
- [ ] Click interactions show risk breakdown
- [ ] Backtest results display
- [ ] Priority list scrolls properly
- [ ] Responsive design works
- [ ] Demo scenario rehearsed

See `DEMO_SCENARIO.md` for the complete demo script and talking points.

## ⚖️ Positioning & Limitations

### What Grease Radar Does
- Identifies recurring wastewater blockage hotspots
- Helps prioritize preventive inspection
- Provides transparent, explainable risk scoring
- Validates approach with historical backtesting

### What Grease Radar Does NOT Do
- Identify guilty businesses or establishments
- Prove grease caused a specific incident
- Replace professional judgment
- Make legal or regulatory determinations
- Guarantee future incidents won't occur

### Current Limitations
- Demo data is synthetic (needs real Vilniaus vandenys data)
- Rule-based model (ML comparison planned)
- Fixed spatial grid size (could be tuned)
- No external data integration (weather, business density, etc.)

### Future Improvements
- Integrate real municipal data
- Add external data sources
- Compare with ML approaches
- Temporal trend analysis
- Automated alerts and notifications
- Mobile field app for inspection teams

## 🤝 Contributing

This is a hackathon project. For production deployment, consider:
- Adding unit tests
- Implementing error handling
- Adding authentication/authorization
- Optimizing for large datasets
- Adding database backend
- Implementing caching
- Adding logging and monitoring

## 📄 License

This project is for Hack4Vilnius. Please contact the team for reuse permissions.

## 🙏 Acknowledgments

- Hack4Vilnius organizers
- Vilniaus vandenys (for providing data access)
- OpenStreetMap contributors
- Leaflet.js library
- Flask and Python community

---

**Built with ❤️ for Hack4Vilnius 2024**
