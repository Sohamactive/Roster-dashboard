# 📊 Roster Processing Dashboard

**Intelligent Analytics Pipeline Workshop**  
HiLabs @ E-Summit IIT Roorkee 2026

## 🎯 Overview

An automated end-to-end analytics pipeline that transforms raw healthcare roster processing data into actionable insights through an interactive dashboard.

### Problem Statement
Transform relational roster processing data into a decision-ready dashboard with minimal manual intervention.

### Solution
A Streamlit-powered dashboard that:
- ✅ Automatically loads and cleans CSV data
- 📊 Computes key operational metrics
- 📈 Visualizes trends, comparisons, and failure patterns
- 🔄 Updates dynamically when data changes
- 🎯 Provides drill-down capabilities by month, market, and state

---

## 🚀 Quick Start (1-Hour Setup)

### Prerequisites
- Python 3.8 or higher
- Windows PowerShell or Command Prompt

### Step 1: Setup Environment

Open PowerShell in the `roster-dashboard` directory and run:

```powershell
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Verify Data Files

Ensure these CSV files are in the project root:
- ✅ `roster_processing_details.csv`
- ✅ `aggregated_operational_metrics.csv`
- ✅ `roster_processing_details_column_description.csv`
- ✅ `aggregated_operational_metrics_column_description.csv`

### Step 3: Launch Dashboard

```powershell
streamlit run app.py
```

The dashboard will automatically open in your default browser at `http://localhost:8501`

---

## 📋 Features

### Key Performance Indicators (KPIs)
- **Total Transactions**: Aggregate record count from roster processing
- **Overall Success Rate**: Percentage of successfully processed records
- **Total Failures**: Count of failed transactions
- **Reprocess Recovery**: Records recovered through reprocessing iterations

### Interactive Visualizations

#### 1. Monthly Success Rate Trend
Line chart showing success rate trends over time to identify patterns and anomalies.

#### 2. First Iteration vs Reprocessing Success
Stacked bar chart comparing initial success vs records recovered through reprocessing, by market.

#### 3. Failure Analysis (Multi-Tab)
- **By State**: Top 10 states with highest failure counts
- **By Organization**: Top 10 organizations with most failures
- **By Line of Business**: Failure distribution across LOBs (Medicare, Medicaid, Commercial)

#### 4. Failed Roster Runs Table
Detailed drillable table showing:
- Roster Object ID
- Organization name
- State
- Line of Business
- Run number (iteration count)
- Total/Success/Failure counts
- Success percentage
- Load health status

### Filters & Controls
- **Month Selector**: Focus on specific reporting periods
- **Market Filter**: Drill down to regional markets
- **State Filter**: Analyze specific geographic areas
- **Download Button**: Export failure details to CSV

---

## 📊 Data Sources

### 1. Roster Processing Details (`roster_processing_details.csv`)
Event-level roster file processing records containing:
- Processing metadata (RO_ID, organization, state, LOB)
- Volume metrics (total, success, fail, skip, reject counts)
- Run iteration details
- Processing stage durations
- Health indicators

**Key Columns Used:**
- `ORG_NM`, `CNT_STATE`, `LOB` — Dimensions
- `RUN_NO` — Processing iteration
- `TOT_REC_CNT`, `SCS_REC_CNT`, `FAIL_REC_CNT` — Volume metrics
- `SCS_PCT`, `SPS_LOAD_HEALTH` — Quality indicators

### 2. Aggregated Operational Metrics (`aggregated_operational_metrics.csv`)
Monthly rollups by market showing:
- First iteration success/fail counts
- Next iteration (reprocessing) success/fail counts
- Overall success/fail totals
- Success percentage

**Key Columns Used:**
- `MONTH`, `MARKET` — Time and regional dimensions
- `FIRST_ITER_SCS_CNT`, `FIRST_ITER_FAIL_CNT` — Initial processing
- `NEXT_ITER_SCS_CNT`, `NEXT_ITER_FAIL_CNT` — Reprocessing results
- `OVERALL_SCS_CNT`, `OVERALL_FAIL_CNT`, `SCS_PERCENT` — Totals

---

## 🔄 How It Works

### Data Pipeline Architecture

```
CSV Files (Raw Data)
        ↓
Data Loading & Validation
        ↓
Data Cleaning & Normalization
   • Type coercion
   • Date parsing
   • Missing value handling
   • Format standardization
        ↓
Metric Computation
   • KPI aggregation
   • Trend calculation
   • Failure analysis
        ↓
Visualization Layer (Plotly)
        ↓
Interactive Dashboard (Streamlit)
```

### Auto-Update Mechanism
- Dashboard reads CSVs on every app refresh
- Press **R** in the browser to reload data
- Streamlit's `@st.cache_data` decorator optimizes performance
- File changes are detected automatically on page refresh

---

## 🛠️ Technical Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Language** | Python 3.8+ | Core processing |
| **Dashboard** | Streamlit | Web interface |
| **Data Processing** | Pandas | CSV loading & manipulation |
| **Visualization** | Plotly | Interactive charts |
| **Environment** | venv | Dependency isolation |

---

## 📖 Usage Examples

### Scenario 1: Identify Problem Markets
1. Navigate to the "First Iteration vs Reprocessing Success" chart
2. Look for markets with large blue (reprocessing) bars
3. These markets have high initial failure rates requiring multiple iterations

### Scenario 2: Drill Down to Specific Failures
1. Use the **Month** and **State** filters in the sidebar
2. Navigate to the "Failed Roster Runs" table at the bottom
3. Sort by failure count to identify problematic organizations
4. Download CSV for detailed investigation

### Scenario 3: Track Success Rate Trends
1. View the "Monthly Success Rate Trend" chart
2. Identify months with drops in success rate
3. Cross-reference with the failure analysis tabs to find root causes

---

## 🧪 Testing & Validation

### Quick Smoke Test

After launching the dashboard, verify:
- ✅ KPI tiles show non-zero values
- ✅ Monthly trend chart displays multiple months
- ✅ Filter dropdowns populate with data
- ✅ Failure tables show recent records
- ✅ Download button generates CSV

### Data Integrity Check

Compare dashboard totals with CSV:
```python
import pandas as pd

# Load aggregated metrics
df = pd.read_csv('aggregated_operational_metrics.csv')

# Get latest month total
latest = df[df['MONTH'] == '01-2026']
total = latest['OVERALL_SCS_CNT'].sum() + latest['OVERALL_FAIL_CNT'].sum()

print(f"Expected total transactions: {total:,}")
```

This should match the "Total Transactions" KPI on the dashboard.

---

## 🔧 Troubleshooting

### Issue: Dashboard won't start
**Solution**: Ensure virtual environment is activated
```powershell
.venv\Scripts\activate
```

### Issue: "No data available" error
**Solution**: Verify CSV files are in the project root directory
```powershell
ls *.csv
```

### Issue: Charts not displaying
**Solution**: Check data format in CSVs, especially MONTH column format

### Issue: Filters show "Unknown" values
**Solution**: CSV may have missing/null values — this is expected and handled

---

## 📦 Project Structure

```
roster-dashboard/
│
├── app.py                                          # Main Streamlit application
├── requirements.txt                                # Python dependencies
├── README.md                                       # This file
│
├── roster_processing_details.csv                  # Raw event-level data
├── aggregated_operational_metrics.csv             # Monthly aggregated data
├── roster_processing_details_column_description.csv
├── aggregated_operational_metrics_column_description.csv
│
└── .venv/                                          # Virtual environment (created)
```

---

## 🎓 Workshop Learning Outcomes

By completing this workshop, participants have:
1. ✅ Built an end-to-end data pipeline from raw CSV to dashboard
2. ✅ Implemented automated data cleaning and normalization
3. ✅ Created interactive visualizations with Plotly
4. ✅ Designed user-friendly analytics interfaces with Streamlit
5. ✅ Applied real-world operational analytics patterns
6. ✅ Experienced minimal-intervention automation principles

---

## 🚀 Future Enhancements (Beyond 1-Hour Workshop)

### Additional Features to Consider
- 🗺️ **Geographic Map View**: State-level choropleth map of success rates
- ⏱️ **Processing Duration Analysis**: Histogram of stage-wise durations
- 🚨 **Alert System**: Configurable thresholds for failure rates
- 📧 **Automated Reporting**: Scheduled email reports with key findings
- 🔗 **Database Integration**: Connect to live databases instead of CSVs
- 🎯 **Predictive Analytics**: ML models to forecast failure risks
- 👥 **Multi-User Access**: Authentication and role-based views
- 📱 **Mobile Responsive**: Optimize for mobile devices

### Code Improvements
- Unit tests for data processing functions
- Error logging and monitoring
- Performance optimization for large datasets
- Configuration file for customizable settings
- Docker containerization for deployment

---

## 📞 Support & Resources

### Workshop Support
- **Event**: E-Summit IIT Roorkee 2026
- **Organizer**: HiLabs
- **Date**: February 8, 2026

### Documentation
- [Streamlit Docs](https://docs.streamlit.io)
- [Pandas Guide](https://pandas.pydata.org/docs/)
- [Plotly Python](https://plotly.com/python/)

---

## 📄 License

Workshop Educational Material  
© 2026 HiLabs - E-Summit IIT Roorkee

---

**Built with ❤️ for Healthcare Data Analytics Education**
#   R o s t e r - d a s h b o a r d  
 