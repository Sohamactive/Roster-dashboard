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

### Step 3: Launch Dashboard

```powershell
streamlit run app.py
```

The dashboard will automatically open in your default browser at `http://localhost:8501`

---

## 📋 Features

### Key Performance Indicators (KPIs)
- **Total Transactions**: Sum of successful and failed roster processing records
- **Overall Success Rate**: Percentage of successfully processed rosters
- **Total Failures**: Count of failed roster processing runs
- **Reprocess Recovery**: Records recovered through subsequent processing iterations

### Interactive Visualizations

#### 1. Monthly Success Rate Trend
Line chart showing success rate trends over time to identify patterns and anomalies.

#### 2. First Iteration vs Reprocessing Success
Stacked bar chart comparing initial success vs records recovered through reprocessing, by market (Top 10 markets by volume).

#### 3. Processing Stage Analysis
- **Stage Distribution**: Bar chart showing roster counts at each processing stage
- **Duration Analysis**: Box plot showing processing time distribution across stages (Pre-Processing, ISF Generation, DART Generation, SPS Load)

#### 4. Failure Analysis (Multi-Tab)
- **By State**: Top 10 states with highest failure counts
- **By Organization**: Top 10 organizations with most failures
- **By Line of Business**: Failure distribution across LOBs (Medicare, Medicaid, Commercial)

#### 5. Failed Roster Details Table
Detailed drillable table showing:
- Roster Object ID (RO_ID)
- Organization name
- State
- Line of Business
- Run number (iteration count)
- Failure status
- Latest processing stage
- SPS Load health status
- Stuck indicator
- Latest run date

### Filters & Controls
- **Month Selector**: Focus on specific reporting periods
- **Market Filter**: Drill down to regional markets
- **State Filter**: Analyze specific geographic areas
- **Download Button**: Export failure details to CSV with timestamp

---

## 📊 Data Sources

### 1. Roster Processing Details (`roster_processing_details.csv`)
Granular roster file processing records containing:
- Processing metadata (RO_ID, organization, state, LOB, source system)
- Run iteration details (RUN_NO)
- Processing stage information (LATEST_STAGE_NM)
- Failure indicators (IS_FAILED, IS_STUCK, FAILURE_STATUS)
- Stage-specific durations (PRE_PROCESSING, ISF_GEN, DART_GEN, SPS_LOAD)
- Health indicators (PRE_PROCESSING_HEALTH, ISF_GEN_HEALTH, DART_GEN_HEALTH, SPS_LOAD_HEALTH)
- Timestamps (FILE_RECEIVED_DT, LATEST_OBJECT_RUN_DT, CREAT_DT, LAST_UPDT_DT)

**Key Columns Used:**
- `RO_ID`, `ORG_NM`, `CNT_STATE`, `LOB` — Dimensions
- `RUN_NO` — Processing iteration count
- `IS_FAILED`, `IS_STUCK` — Failure indicators
- `LATEST_STAGE_NM` — Current processing stage
- `*_DURATION` columns — Performance metrics
- `*_HEALTH` columns — Stage quality indicators

### 2. Aggregated Operational Metrics (`aggregated_operational_metrics.csv`)
Monthly rollups by market and client showing:
- First iteration success/fail counts
- Next iteration (reprocessing) success/fail counts
- Overall success/fail totals
- Success percentage

**Key Columns Used:**
- `MONTH`, `MARKET`, `CLIENT_ID` — Dimensions
- `FIRST_ITER_SCS_CNT`, `FIRST_ITER_FAIL_CNT` — Initial processing results
- `NEXT_ITER_SCS_CNT`, `NEXT_ITER_FAIL_CNT` — Reprocessing results
- `OVERALL_SCS_CNT`, `OVERALL_FAIL_CNT`, `SCS_PERCENT` — Aggregated totals

---

## 🔄 How It Works

### Data Pipeline Architecture

```
CSV Files (Raw Data)
        ↓
Data Loading & Validation
        ↓
Data Cleaning & Normalization
   • Type coercion (numeric, dates, text)
   • Date parsing with error handling
   • Missing value imputation
   • Format standardization
        ↓
Metric Computation
   • KPI aggregation
   • Trend calculation
   • Failure analysis by dimension
        ↓
Visualization Layer (Plotly)
   • Line charts, bar charts, box plots
   • Interactive hover & zoom
        ↓
Interactive Dashboard (Streamlit)
   • Dynamic filtering
   • Real-time updates
```

### Auto-Update Mechanism
- Dashboard reads CSVs on every app refresh
- Press **R** in the browser to reload data after CSV updates
- Streamlit's `@st.cache_data` decorator caches processed data for performance
- File changes are detected automatically on page refresh

---

## 🛠️ Technical Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Language** | Python 3.8+ | Core processing |
| **Dashboard** | Streamlit | Web interface |
| **Data Processing** | Pandas | CSV loading & manipulation |
| **Visualization** | Plotly Express & Graph Objects | Interactive charts |
| **Environment** | venv | Dependency isolation |

---

## 📖 Usage Examples

### Scenario 1: Identify Problem Markets
1. Navigate to the "First Iteration vs Reprocessing Success" chart
2. Look for markets with large blue (recovery) bars relative to green (first iteration)
3. These markets have high initial failure rates requiring multiple reprocessing iterations

### Scenario 2: Drill Down to Specific Failures
1. Use the **Month** and **State** filters in the sidebar
2. Navigate to the "Failed Roster Analysis" tabs
3. Click on the "Failed Roster Details" table at the bottom
4. Click **Download Failed Roster Details (CSV)** for detailed investigation

### Scenario 3: Track Success Rate Trends
1. View the "Monthly Success Rate Trend" chart
2. Identify months with drops in success rate
3. Cross-reference with the failure analysis tabs to find root causes (state, org, LOB)

### Scenario 4: Analyze Processing Performance
1. Review the "Processing Duration Distribution by Stage" box plot
2. Identify stages with high median durations or wide variability
3. Focus optimization efforts on bottleneck stages

---

## 🧪 Testing & Validation

### Quick Smoke Test

After launching the dashboard, verify:
- ✅ Four KPI tiles show non-zero values with gradient backgrounds
- ✅ "Monthly Success Rate Trend" chart displays multiple data points
- ✅ Filter dropdowns populate with available options
- ✅ Failure analysis tabs show charts or success messages
- ✅ Failed Roster Details table shows recent records (if failures exist)
- ✅ Download button generates timestamped CSV

### Data Integrity Check

Compare dashboard totals with CSV:
```python
import pandas as pd

# Load aggregated metrics
df = pd.read_csv('aggregated_operational_metrics.csv')

# Get latest month
df['MONTH_DT'] = pd.to_datetime(df['MONTH'], format='%m-%Y', errors='coerce')
latest_month = df['MONTH_DT'].max()
latest = df[df['MONTH_DT'] == latest_month]

# Calculate total
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
**Solution**: Verify both CSV files are in the project root directory
```powershell
dir *.csv
```
Expected files: `roster_processing_details.csv` and `aggregated_operational_metrics.csv`

### Issue: Charts not displaying
**Solution**: 
- Check MONTH column format in `aggregated_operational_metrics.csv` (should be MM-YYYY)
- Ensure numeric columns contain valid numbers (no text values)
- Verify date columns are in recognizable date formats

### Issue: Filters show "Unknown" values
**Solution**: This is expected for missing/null values in CSV — the app handles this gracefully

### Issue: KPIs show zero or incorrect values
**Solution**: 
- Verify column names match expected format (case-sensitive)
- Check for null values in critical columns
- Ensure IS_FAILED column uses 1 for failures, 0 for success

---

## 📦 Project Structure

```
roster-dashboard/
│
├── app.py                                 # Main Streamlit application
├── requirements.txt                       # Python dependencies
├── README.md                              # This file
│
├── roster_processing_details.csv         # Granular processing data
├── aggregated_operational_metrics.csv    # Monthly aggregated data
│
└── .venv/                                 # Virtual environment (created during setup)
```

---

## 📋 Dependencies

The application requires the following Python packages (defined in `requirements.txt`):

```text
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.17.0
```

Install with:
```powershell
pip install -r requirements.txt
```

---

## 🎓 Workshop Learning Outcomes

By completing this workshop, participants have:
1. ✅ Built an end-to-end data pipeline from raw CSV to interactive dashboard
2. ✅ Implemented automated data cleaning and normalization techniques
3. ✅ Created interactive visualizations with Plotly Express and Graph Objects
4. ✅ Designed user-friendly analytics interfaces with Streamlit
5. ✅ Applied real-world operational analytics patterns
6. ✅ Experienced minimal-intervention automation principles
7. ✅ Learned data-driven decision making through visual analytics

---

## 🚀 Future Enhancements (Beyond 1-Hour Workshop)

### Additional Features to Consider
- 🗺️ **Geographic Map View**: State-level choropleth map of success rates
- 📊 **Advanced Analytics**: Statistical outlier detection for abnormal failure patterns
- 🚨 **Alert System**: Configurable thresholds with notifications for critical failures
- 📧 **Automated Reporting**: Scheduled email reports with key findings
- 🔗 **Database Integration**: Connect to live databases instead of static CSVs
- 🎯 **Predictive Analytics**: ML models to forecast failure risks
- 👥 **Multi-User Access**: Authentication and role-based views
- 📱 **Mobile Responsive**: Optimized layout for mobile devices
- 🔍 **Search Functionality**: Full-text search across roster details
- 📈 **Time Series Forecasting**: Predict future success rates

### Code Improvements
- Unit tests for data processing functions
- Error logging and monitoring with log files
- Performance optimization for datasets >100K rows
- Configuration file (YAML/JSON) for customizable settings
- Docker containerization for easy deployment
- CI/CD pipeline for automated testing and deployment

---

## 📞 Support & Resources

### Workshop Support
- **Event**: E-Summit IIT Roorkee 2026
- **Organizer**: HiLabs
- **Date**: February 8, 2026

### Documentation
- [Streamlit Documentation](https://docs.streamlit.io)
- [Pandas User Guide](https://pandas.pydata.org/docs/user_guide/index.html)
- [Plotly Python Graphing Library](https://plotly.com/python/)

### Troubleshooting Resources
- [Streamlit Community Forum](https://discuss.streamlit.io/)
- [Stack Overflow - Streamlit Tag](https://stackoverflow.com/questions/tagged/streamlit)

---

## 📄 License

Workshop Educational Material  
© 2026 HiLabs - E-Summit IIT Roorkee

---

**Built with ❤️ for Healthcare Data Analytics Education**
