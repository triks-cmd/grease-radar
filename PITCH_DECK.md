# Grease Radar — Pitch Deck Outline

## Slide 1: Title Slide

**Grease Radar**
*Prevent Wastewater Blockages Before They Happen*

Hack4Vilnius · Challenge 12

---

## Slide 2: The Problem

**Cities React to Blockages After They Occur**

Current situation:
- Emergency response to blockages
- Service disruptions for residents and businesses
- High maintenance costs
- Reactive, not proactive

Impact:
- Expensive emergency repairs
- Unplanned service outages
- Inefficient resource allocation
- Environmental risks

---

## Slide 3: The Opportunity

**Historical Data Contains Predictive Patterns**

Every blockage tells a story:
- Where it happened
- When it happened
- How often it happens in the same area

These patterns can predict future problems.

**Insight**: Instead of waiting for the next blockage, we can identify high-risk areas and take preventive action.

---

## Slide 4: Our Solution

**Grease Radar: From Reacting to Predicting**

A preventive monitoring system that:
1. Analyzes historical incident data
2. Identifies high-risk hotspot areas
3. Calculates transparent risk scores
4. Prioritizes preventive inspection

**Result**: Data-driven decisions that prevent problems before they occur.

---

## Slide 5: How It Works

**Transparent, Explainable Risk Scoring**

For each area, we calculate four factors:

| Factor | Weight | What It Measures |
|--------|--------|-----------------|
| Frequency | 35% | Number of incidents |
| Recurrence | 30% | How many different months |
| Recency | 20% | How recently incidents occurred |
| Spatial Density | 15% | Nearby incident cells |

Overall Risk Score: 0-100
- HIGH (≥70): Immediate attention
- MEDIUM (≥40): Monitor closely
- LOW (<40): Routine inspection

---

## Slide 6: Technical Approach

**Spatial Grid Analysis**

1. Divide city into grid cells (~500m)
2. Aggregate incidents by cell
3. Calculate metrics for each cell
4. Compute risk score
5. Rank and prioritize hotspots

**No black-box AI** - fully transparent rule-based model that anyone can understand and audit.

---

## Slide 7: Validation

**Backtested on Historical Data**

Methodology:
- 70-30 temporal train-test split
- Train on earlier incidents
- Identify top 20% risk cells
- Test: measure future incident capture

Results: [Insert actual backtest percentage from demo]

**This shows our approach can effectively predict where future problems are likely to occur.**

---

## Slide 8: The Product

**Web-Based Municipal Monitoring Tool**

Features:
- Interactive Vilnius map with incident visualization
- Color-coded risk hotspots
- Detailed risk breakdown for each area
- Priority list for systematic inspection
- One-click CSV import for official data
- Historical backtesting dashboard

**Professional UI designed for municipal workflows.**

---

## Slide 9: Value Proposition

**Benefits for Vilnius**

1. **Cost Savings**: Preventive maintenance < Emergency response
2. **Service Reliability**: Fewer disruptions for residents and businesses
3. **Resource Optimization**: Teams focus on high-priority areas
4. **Data-Driven Decisions**: Move from reactive to proactive
5. **Transparency**: Explainable model builds trust

---

## Slide 10: Implementation

**Easy Integration**

Current state:
- Working web prototype
- Demo data included
- CSV import ready for official data
- REST API for system integration

Next steps:
- Integrate real Vilniaus vandenys data
- Tune model parameters
- Add external data sources (optional)
- Pilot program with municipal teams

---

## Slide 11: Competitive Advantage

**Why Grease Radar?**

| Aspect | Grease Radar | Alternatives |
|--------|--------------|--------------|
| Transparency | ✅ Fully explainable | ❌ Black-box AI |
| Validation | ✅ Backtested | ❌ Unvalidated |
| Focus | ✅ Single clear use case | ❌ Overly complex |
| Practicality | ✅ Built for workflows | ❌ Research-focused |
| Cost | ✅ Lightweight web app | ❌ Expensive enterprise software |

---

## Slide 12: Roadmap

**Future Enhancements**

Phase 1 (Current):
- ✅ Rule-based risk model
- ✅ Interactive map
- ✅ Backtesting validation

Phase 2:
- Integrate real municipal data
- Add external data sources (weather, business density)
- Compare with ML approaches

Phase 3:
- Automated alerts and notifications
- Mobile field app for inspection teams
- Advanced temporal trend analysis

---

## Slide 13: Team & Ask

**What We Need**

For immediate impact:
- Access to official Vilniaus vandenys incident data
- Feedback from municipal operations teams
- Pilot program opportunity

For long-term success:
- Integration with existing municipal systems
- Funding for Phase 2 enhancements
- Partnership for ongoing development

---

## Slide 14: Conclusion

**Grease Radar: Prevent Problems Before They Occur**

Transform reactive maintenance into proactive prevention.

**Key Takeaways:**
- Historical data contains predictive patterns
- Transparent risk scoring builds trust
- Backtesting validates the approach
- Easy to implement and integrate
- Real value for the city

**Thank you!**

Questions?

---

## Speaker Notes

### Slide 2 (Problem)
Emphasize the emotional and financial impact of reactive maintenance. Use concrete examples if possible.

### Slide 3 (Opportunity)
This is the "aha" moment - help the audience see that they already have the data they need.

### Slide 5 (How It Works)
Walk through the example calculation slowly. Show the risk breakdown in the demo.

### Slide 7 (Validation)
This is crucial - it proves the approach works, not just that it sounds good.

### Slide 9 (Value)
Focus on the "so what?" - why should Vilnius care about this?

### Slide 13 (Team & Ask)
Be specific about what you need. Don't just say "we need support" - say exactly what would help.

---

## Presentation Tips

1. **Show, Don't Just Tell**: Use the live demo extensively
2. **Tell a Story**: Start with the problem, show the solution, end with impact
3. **Be Honest About Limitations**: Transparency builds credibility
4. **Focus on Value**: Not just how it works, but why it matters
5. **Keep It Simple**: Avoid jargon, explain technical concepts clearly
6. **Time Management**: 5-7 minutes for pitch, 3-5 minutes for Q&A
7. **Practice**: Rehearse the demo scenario multiple times

---

## Demo Integration

**During the presentation:**
- After Slide 6, show the map and explain hotspots
- After Slide 5, click a hotspot and show risk breakdown
- After Slide 7, show the backtest results
- After Slide 8, show the priority list

This makes the presentation interactive and memorable.

---

## Backup Slides (Optional)

### Backup 1: Technical Architecture
- Detailed system diagram
- Data flow explanation
- Technology stack

### Backup 2: Risk Calculation Example
- Step-by-step calculation for a specific hotspot
- Show the math behind the score

### Backup 3: Backtesting Methodology
- Detailed explanation of train-test split
- Statistical validation approach
- Comparison with baseline

### Backup 4: Data Requirements
- Exact CSV format specification
- Required vs optional fields
- Data quality considerations

### Backup 5: Security & Privacy
- Data handling practices
- No business identification
- Compliance with regulations

---

## Q&A Preparation

### Common Questions

**Q: How accurate is the model?**
A: Our backtesting shows [X]% capture rate on future incidents. This is a strong baseline using only historical data. With additional data sources, we could improve further.

**Q: What data do you need?**
A: We need incident data with latitude, longitude, and date. Additional fields are optional. We've built CSV import to make this easy.

**Q: Can this replace human judgment?**
A: No, it's a decision support tool. It helps prioritize where to focus attention, but doesn't replace professional judgment.

**Q: How do you handle false positives?**
A: The system recommends areas for inspection, not action. Inspectors assess the actual situation and decide what to do.

**Q: What about seasonal patterns?**
A: Our current model includes recency which captures some temporal patterns. Future versions could explicitly model seasonality.

**Q: Is this only for grease-related blockages?**
A: It works for any type of wastewater blockage. The approach is generalizable to different incident types.

**Q: How much does it cost to implement?**
A: The prototype is lightweight and low-cost. Main costs would be integration work and any additional data sources. Significantly cheaper than emergency response costs.

**Q: What if the data is incomplete?**
A: The system works with whatever data is available. More data = better predictions, but the approach works even with limited data.

**Q: Can other cities use this?**
A: Yes, the approach is generalizable. Just need incident data with coordinates and dates.

**Q: Why not use machine learning?**
A: We started with a transparent rule-based model for explainability. ML comparison is planned - we want to see if it actually improves performance.

---

## Success Criteria

Judges should walk away understanding:
1. ✅ The problem is real and costly
2. ✅ Our solution is practical and implementable
3. ✅ The approach is validated (backtesting)
4. ✅ The model is transparent and explainable
5. ✅ There's clear value for the city
6. ✅ We have a working prototype, not just an idea
7. ✅ We know the next steps for implementation

Perfect outcome:
- Interest in pilot program
- Questions about implementation details (not the concept)
- Recognition of practical value
- Request for follow-up meeting
