# Grease Radar — Demo Scenario for Hack4Vilnius

## Quick Demo Script (2-3 minutes)

### Step 1: Introduction (30 seconds)
**Open Grease Radar** at http://127.0.0.1:5000

**Say:**
"Grease Radar is a preventive monitoring system for wastewater blockages. Instead of reacting to blockages after they happen, we help cities identify high-risk areas and prioritize preventive inspection."

### Step 2: Show the Map (30 seconds)
**Point to the map**

**Say:**
"This is Vilnius. Each circle represents a hotspot area where blockages have occurred historically. The size and color indicate risk level - red is high risk, orange is medium, green is low."

### Step 3: Show Statistics (20 seconds)
**Point to the stats cards**

**Say:**
"Our system processes all historical incidents. Here we can see the total number of incidents, how many high-risk hotspots we've identified, and the data period we're analyzing."

### Step 4: Explain Risk Score (45 seconds)
**Click on a high-risk hotspot (first one in the list)**

**Say:**
"When we click on a hotspot, we get a detailed breakdown of why it's considered high-risk. Our risk score is transparent and explainable."

**Point to the risk breakdown:**
- "Frequency: how many incidents occurred in this area"
- "Recurrence: how many different months had incidents"
- "Recency: how recently the last incident occurred"
- "Spatial density: how many nearby cells also have incidents"

**Point to the risk bar:**
"This bar shows exactly how each factor contributes to the overall score. 35% from frequency, 30% from recurrence, 20% from recency, and 15% from spatial density."

### Step 5: Show Recommended Action (15 seconds)
**Point to the action box**

**Say:**
"Based on this analysis, the system recommends prioritizing preventive inspection in this area. Importantly, we don't identify specific businesses - we just flag areas that need attention."

### Step 6: Demonstrate Backtesting (30 seconds)
**Point to the backtest panel**

**Say:**
"We've validated our approach using historical backtesting. We trained the model on 70% of the data, then tested it on the remaining 30% to see if it could predict future incidents."

**Read the results:**
"Our model captured X% of future incidents within the top-risk cells. This shows that our approach can effectively identify areas where future problems are likely to occur."

### Step 7: Priority List (20 seconds)
**Point to the priority list**

**Say:**
"This list shows all hotspots ranked by risk score. Municipal teams can work through this list systematically, focusing on the highest-risk areas first."

### Step 8: Transparency (20 seconds)
**Point to the Transparent Risk Score section**

**Say:**
"Our model is fully transparent - no black-box AI. We use a rule-based approach that anyone can understand and audit. The weights we use are a baseline for validation."

### Step 9: Conclusion (30 seconds)
**Say:**
"Grease Radar transforms reactive maintenance into proactive prevention. By identifying high-risk areas before the next blockage occurs, cities can:

1. Reduce emergency response costs
2. Minimize service disruptions
3. Extend infrastructure lifespan
4. Optimize resource allocation

We're not just mapping blockages - we're enabling data-driven preventive action."

---

## Extended Demo (if judges ask questions)

### Q: How does the system work technically?

**A:**
"We use a spatial grid system to divide the city into cells. For each cell, we calculate four metrics:
- Frequency: number of incidents
- Recurrence: number of distinct months with incidents
- Recency: exponential decay based on time since last incident
- Spatial density: count of neighboring cells with incidents

These are combined using weighted averages to produce a risk score from 0-100. The system automatically identifies hotspots and ranks them by risk."

### Q: What data do you need?

**A:**
"We need incident data with three required fields: latitude, longitude, and date. Additional fields like incident type, severity, or description can be included but aren't required. The system is designed to work with whatever municipal data is available."

### Q: How accurate is the backtesting?

**A:**
"Our backtesting shows that X% of future incidents occurred in cells that the model identified as top-risk. This is a strong baseline performance using only historical incident data. With additional data sources (weather, restaurant density, etc.), we could potentially improve this further."

### Q: Can this be integrated with existing systems?

**A:**
"Yes. The system is built as a lightweight web application with a REST API. It can be integrated with existing municipal GIS systems, work order management systems, or used as a standalone tool. The CSV import makes it easy to update with new data."

### Q: What are the limitations?

**A:**
"Current limitations:
- We use demo data for this prototype - real Vilniaus vandenys data would be needed for production
- The model is rule-based, not machine learning (though we could add ML comparison)
- We don't include external factors like weather, seasonality, or business density
- The spatial grid size is fixed at 0.005 degrees - this could be tuned

However, these are all improvement opportunities, not fundamental limitations."

### Q: What's next for Grease Radar?

**A:**
"Next steps:
1. Integrate real Vilniaus vandenys incident data
2. Add external data sources (restaurant locations, weather patterns)
3. Compare rule-based model with ML approaches
4. Add temporal trend analysis
5. Implement automated alerts and notifications
6. Build mobile field app for inspection teams"

---

## Key Talking Points

### Problem
- Cities currently react to blockages after they occur
- This is expensive, disruptive, and inefficient
- Historical data contains patterns that can predict future problems

### Solution
- Grease Radar identifies high-risk areas before the next blockage
- Transparent, explainable risk scoring
- Backtested on historical data
- Easy to integrate with existing systems

### Value
- **Cost savings**: Preventive maintenance is cheaper than emergency response
- **Service reliability**: Fewer disruptions for residents and businesses
- **Resource optimization**: Teams focus on high-priority areas
- **Data-driven decisions**: Move from reactive to proactive

### Differentiation
- **Transparent**: No black-box AI - explainable risk factors
- **Validated**: Backtested on historical data
- **Practical**: Built for municipal workflows, not research
- **Focused**: Single clear use case, not trying to do everything

---

## Technical Architecture

### Backend
- Flask web framework
- Pandas for data processing
- NumPy for calculations
- Spatial grid-based hotspot detection

### Frontend
- Leaflet.js for interactive maps
- Vanilla JavaScript (no framework overhead)
- Responsive CSS design

### Data Pipeline
1. CSV import (official data or demo)
2. Validation and cleaning
3. Spatial grid aggregation
4. Risk score calculation
5. Hotspot ranking
6. Backtesting validation
7. API response to frontend

### Key Algorithms
- **Spatial grid**: 0.005-degree cells (~500m)
- **Min-max normalization**: For fair comparison across metrics
- **Exponential decay**: For recency scoring (180-day half-life)
- **Quantile threshold**: Top 20% for backtesting
- **Train-test split**: 70-30 temporal split for validation

---

## Preparation Checklist

Before the demo:
- [ ] Server running on http://127.0.0.1:5000
- [ ] Demo data loaded (or official data if available)
- [ ] Map loads correctly
- [ ] All hotspots display
- [ ] Click interactions work
- [ ] Backtest results display
- [ ] Risk breakdown calculations visible
- [ ] Priority list scrolls properly
- [ ] Responsive design works on screen

Have ready:
- [ ] Demo scenario printed or memorized
- [ ] Answers to common questions prepared
- [ ] Technical architecture documentation
- [ ] Contact info for follow-up

---

## Backup Plans

### If demo data doesn't load
- Use the built-in demo data (it's already loaded)
- Explain that real data integration is straightforward via CSV import

### If map doesn't display
- Check internet connection (OpenStreetMap tiles require internet)
- Have screenshots ready as backup

### If backtesting shows low results
- Explain that this is baseline performance with demo data
- Real data would likely show better patterns
- Model can be tuned with different weights or algorithms

### If judges ask about ML
- Explain that we started with transparent rule-based model
- ML comparison is planned but not required for MVP
- Transparency is a feature, not a limitation

---

## Success Metrics for Demo

Judges should understand:
1. ✅ The problem we're solving
2. ✅ How our solution works
3. ✅ Why it's valuable to the city
4. ✅ That it's technically feasible
5. ✅ That it's been validated (backtesting)
6. ✅ That it's transparent and explainable
7. ✅ That it can be implemented realistically

Perfect demo outcome:
- Judges nodding along with the explanation
- Questions about implementation, not about the concept
- Interest in next steps or pilot program
- Recognition of the practical value
