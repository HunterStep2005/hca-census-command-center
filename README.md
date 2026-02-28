# HCA Census Command Center

Hospital census dashboard for HCA Healthcare — built for the UA Innovate Hackathon (Prototype Innovation category).

## Features
- **Executive Overview**: System-wide KPIs, facility status cards sorted by occupancy, sparklines, 72h peak projections
- **Facility Drill-Down**: Interactive Chart.js charts with historical + forecast data, confidence intervals, capacity reference lines
- **Configurable Alerts**: Per-facility threshold rules, cooldown periods, active alert feed with snooze
- **Settings**: Dark mode, PDF/CSV/link export, role-based access simulation, AI transparency section

## Tech Stack
- Vanilla HTML/CSS/JavaScript (single-page app)
- Chart.js for data visualization
- Holt-Winters Exponential Smoothing for 72-hour forecasts
- Mobile-first responsive design

## Running Locally
1. Clone this repo
2. Open `index.html` in a browser (or use a local server like `python -m http.server`)
3. The app loads `data.json` automatically

## Data
- 10 HCA facilities across the US
- 5 metrics tracked every 15 minutes: Admissions, Births, Discharges, ICU Occupancy, Total Census
- Date range: Jan 1 – Feb 6, 2026
- Forecasts generated using Holt-Winters Exponential Smoothing with 24h seasonal period