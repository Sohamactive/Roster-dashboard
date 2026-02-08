"""
Roster Dashboard - Intelligent Analytics Pipeline
HiLabs Workshop @ E-Summit IIT Roorkee
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# Page configuration
st.set_page_config(
    page_title="Roster Processing Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    /* Enhanced KPI Card Styling */
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
    }
    
    div[data-testid="stMetricLabel"] {
        font-size: 1rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Individual metric containers with gradient backgrounds */
    div[data-testid="column"]:nth-of-type(1) div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
        border: 2px solid rgba(255, 255, 255, 0.2);
    }
    
    div[data-testid="column"]:nth-of-type(1) div[data-testid="stMetricValue"],
    div[data-testid="column"]:nth-of-type(1) div[data-testid="stMetricLabel"] {
        color: white !important;
    }
    
    div[data-testid="column"]:nth-of-type(2) div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 8px 20px rgba(17, 153, 142, 0.4);
        border: 2px solid rgba(255, 255, 255, 0.2);
    }
    
    div[data-testid="column"]:nth-of-type(2) div[data-testid="stMetricValue"],
    div[data-testid="column"]:nth-of-type(2) div[data-testid="stMetricLabel"] {
        color: white !important;
    }
    
    div[data-testid="column"]:nth-of-type(3) div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 8px 20px rgba(235, 51, 73, 0.4);
        border: 2px solid rgba(255, 255, 255, 0.2);
    }
    
    div[data-testid="column"]:nth-of-type(3) div[data-testid="stMetricValue"],
    div[data-testid="column"]:nth-of-type(3) div[data-testid="stMetricLabel"] {
        color: white !important;
    }
    
    div[data-testid="column"]:nth-of-type(4) div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 8px 20px rgba(240, 147, 251, 0.4);
        border: 2px solid rgba(255, 255, 255, 0.2);
    }
    
    div[data-testid="column"]:nth-of-type(4) div[data-testid="stMetricValue"],
    div[data-testid="column"]:nth-of-type(4) div[data-testid="stMetricLabel"] {
        color: white !important;
    }
    
    /* Hover effects */
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        transition: all 0.3s ease;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.3);
    }
    </style>
""", unsafe_allow_html=True)


# ============================================================================
# DATA LOADING & CLEANING
# ============================================================================

@st.cache_data
def load_roster_processing_details():
    """Load and clean roster processing details CSV"""
    try:
        df = pd.read_csv('roster_processing_details.csv')
        
        # Clean numeric columns
        numeric_cols = ['RUN_NO', 'IS_FAILED', 'IS_STUCK', 'FILE_STATUS_CD',
                       'PRE_PROCESSING_DURATION', 'ISF_GEN_DURATION', 
                       'DART_GEN_DURATION', 'SPS_LOAD_DURATION']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # Parse dates
        date_cols = ['FILE_RECEIVED_DT', 'LATEST_OBJECT_RUN_DT', 
                    'CREAT_DT', 'LAST_UPDT_DT']
        for col in date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        
        # Clean text fields
        text_cols = ['RO_ID', 'ORG_NM', 'CNT_STATE', 'LOB', 'SRC_SYS', 
                    'SPS_LOAD_HEALTH', 'FAILURE_STATUS', 'LATEST_STAGE_NM',
                    'PRE_PROCESSING_HEALTH', 'ISF_GEN_HEALTH', 'DART_GEN_HEALTH']
        for col in text_cols:
            if col in df.columns:
                df[col] = df[col].fillna('Unknown').astype(str).str.strip()
        
        return df
    except Exception as e:
        st.error(f"Error loading roster_processing_details.csv: {e}")
        return pd.DataFrame()


@st.cache_data
def load_aggregated_metrics():
    """Load and clean aggregated operational metrics CSV"""
    try:
        df = pd.read_csv('aggregated_operational_metrics.csv')
        
        # Normalize MONTH format (handle MM-YYYY and YYYY-MM)
        if 'MONTH' in df.columns:
            # Convert to datetime and then to standard format
            df['MONTH_DT'] = pd.to_datetime(df['MONTH'], format='%m-%Y', errors='coerce')
            if df['MONTH_DT'].isna().all():
                df['MONTH_DT'] = pd.to_datetime(df['MONTH'], errors='coerce')
            # Handle NaT values before strftime
            df['MONTH'] = df['MONTH_DT'].apply(lambda x: x.strftime('%m-%Y') if pd.notna(x) else 'Unknown')
            df['MONTH_SORT'] = df['MONTH_DT']
        
        # Clean numeric columns
        numeric_cols = ['FIRST_ITER_SCS_CNT', 'FIRST_ITER_FAIL_CNT',
                       'NEXT_ITER_SCS_CNT', 'NEXT_ITER_FAIL_CNT',
                       'OVERALL_SCS_CNT', 'OVERALL_FAIL_CNT', 'SCS_PERCENT']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # Clean text fields
        if 'MARKET' in df.columns:
            df['MARKET'] = df['MARKET'].fillna('Unknown').astype(str).str.strip()
        if 'CLIENT_ID' in df.columns:
            df['CLIENT_ID'] = df['CLIENT_ID'].astype(str)
        
        return df
    except Exception as e:
        st.error(f"Error loading aggregated_operational_metrics.csv: {e}")
        return pd.DataFrame()


# ============================================================================
# METRICS COMPUTATION
# ============================================================================

def compute_kpis(agg_df, roster_df, selected_month=None):
    """Compute key performance indicators"""
    
    # Filter by month if specified
    if selected_month and not agg_df.empty:
        agg_filtered = agg_df[agg_df['MONTH'] == selected_month]
    else:
        # Use latest month
        if not agg_df.empty and 'MONTH_SORT' in agg_df.columns:
            latest_month = agg_df['MONTH_SORT'].max()
            agg_filtered = agg_df[agg_df['MONTH_SORT'] == latest_month]
        else:
            agg_filtered = agg_df
    
    if agg_filtered.empty:
        return {
            'total_transactions': 0,
            'success_rate': 0.0,
            'total_failures': 0,
            'first_iter_success': 0,
            'reprocess_recovery': 0,
            'total_organizations': 0
        }
    
    total_transactions = int(agg_filtered['OVERALL_SCS_CNT'].sum() + agg_filtered['OVERALL_FAIL_CNT'].sum())
    total_failures = int(agg_filtered['OVERALL_FAIL_CNT'].sum())
    total_success = int(agg_filtered['OVERALL_SCS_CNT'].sum())
    success_rate = (total_success / total_transactions * 100) if total_transactions > 0 else 0.0
    
    first_iter_success = int(agg_filtered['FIRST_ITER_SCS_CNT'].sum())
    next_iter_success = int(agg_filtered['NEXT_ITER_SCS_CNT'].sum())
    reprocess_recovery = next_iter_success - first_iter_success
    
    # Organization count from roster details
    total_organizations = roster_df['ORG_NM'].nunique() if not roster_df.empty else 0
    
    return {
        'total_transactions': total_transactions,
        'success_rate': success_rate,
        'total_failures': total_failures,
        'first_iter_success': first_iter_success,
        'reprocess_recovery': reprocess_recovery,
        'total_organizations': total_organizations
    }


# ============================================================================
# VISUALIZATION FUNCTIONS
# ============================================================================

def create_monthly_trend(agg_df):
    """Monthly success rate trend line chart"""
    if agg_df.empty or 'MONTH_SORT' not in agg_df.columns:
        return None
    
    # Aggregate by month
    monthly = agg_df.groupby(['MONTH', 'MONTH_SORT']).agg({
        'OVERALL_SCS_CNT': 'sum',
        'OVERALL_FAIL_CNT': 'sum'
    }).reset_index()
    
    monthly['Success_Rate'] = (
        monthly['OVERALL_SCS_CNT'] / 
        (monthly['OVERALL_SCS_CNT'] + monthly['OVERALL_FAIL_CNT']) * 100
    )
    
    monthly = monthly.sort_values('MONTH_SORT')
    
    fig = px.line(
        monthly, 
        x='MONTH', 
        y='Success_Rate',
        title='Monthly Success Rate Trend',
        labels={'Success_Rate': 'Success Rate (%)', 'MONTH': 'Month'},
        markers=True
    )
    
    fig.update_layout(
        hovermode='x unified',
        yaxis=dict(range=[0, 100]),
        height=400
    )
    
    fig.update_traces(line_color='#1f77b4', line_width=3)
    
    return fig


def create_first_vs_next_iter(agg_df):
    """Stacked bar chart comparing first vs next iteration success by market"""
    if agg_df.empty:
        return None
    
    # Get latest month
    latest_month = agg_df['MONTH_SORT'].max()
    df_latest = agg_df[agg_df['MONTH_SORT'] == latest_month].copy()
    
    # Select top 10 markets by total volume
    df_latest['Total_Volume'] = df_latest['OVERALL_SCS_CNT'] + df_latest['OVERALL_FAIL_CNT']
    top_markets = df_latest.nlargest(10, 'Total_Volume')
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='First Iteration Success',
        x=top_markets['MARKET'],
        y=top_markets['FIRST_ITER_SCS_CNT'],
        marker_color='#2ecc71'
    ))
    
    fig.add_trace(go.Bar(
        name='Recovery (Next Iterations)',
        x=top_markets['MARKET'],
        y=top_markets['NEXT_ITER_SCS_CNT'] - top_markets['FIRST_ITER_SCS_CNT'],
        marker_color='#3498db'
    ))
    
    fig.update_layout(
        title='First Iteration vs Reprocessing Success (Top 10 Markets)',
        barmode='stack',
        xaxis_title='Market',
        yaxis_title='Success Count',
        height=400,
        hovermode='x unified'
    )
    
    return fig


def create_top_failures_chart(roster_df, group_by='CNT_STATE', top_n=10):
    """Bar chart showing top failures by organization, state, or LOB"""
    if roster_df.empty or group_by not in roster_df.columns:
        return None
    
    # Filter for failed rosters (IS_FAILED = 1)
    failed_rosters = roster_df[roster_df['IS_FAILED'] == 1]
    
    if failed_rosters.empty:
        return None
    
    # Count failures by group
    failures = failed_rosters.groupby(group_by).size().reset_index(name='Failure Count')
    failures = failures.sort_values('Failure Count', ascending=False).head(top_n)
    
    fig = px.bar(
        failures,
        x=group_by,
        y='Failure Count',
        title=f'Top {top_n} Failed Rosters by {group_by}',
        labels={'Failure Count': 'Failed Roster Count', group_by: group_by},
        color='Failure Count',
        color_continuous_scale='Reds'
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        height=400,
        showlegend=False
    )
    
    return fig


def create_failure_details_table(roster_df, limit=50):
    """Create a detailed table of failed roster runs"""
    if roster_df.empty:
        return pd.DataFrame()
    
    # Filter for failures (IS_FAILED = 1)
    failures = roster_df[roster_df['IS_FAILED'] == 1].copy()
    
    if failures.empty:
        return pd.DataFrame()
    
    # Sort by recent date
    failures = failures.sort_values('LAST_UPDT_DT', ascending=False)
    
    # Select relevant columns
    display_cols = ['RO_ID', 'ORG_NM', 'CNT_STATE', 'LOB', 'RUN_NO', 
                   'FAILURE_STATUS', 'LATEST_STAGE_NM', 'SPS_LOAD_HEALTH',
                   'IS_STUCK', 'LATEST_OBJECT_RUN_DT']
    
    available_cols = [col for col in display_cols if col in failures.columns]
    
    return failures[available_cols].head(limit)


def create_processing_stage_chart(roster_df):
    """Bar chart showing processing stage distribution"""
    if roster_df.empty or 'LATEST_STAGE_NM' not in roster_df.columns:
        return None
    
    # Count rosters by stage
    stage_counts = roster_df['LATEST_STAGE_NM'].value_counts().reset_index()
    stage_counts.columns = ['Stage', 'Count']
    
    fig = px.bar(
        stage_counts,
        x='Stage',
        y='Count',
        title='Roster Distribution by Processing Stage',
        labels={'Count': 'Number of Rosters', 'Stage': 'Processing Stage'},
        color='Count',
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        height=400,
        showlegend=False
    )
    
    return fig


def create_duration_analysis(roster_df):
    """Box plot showing processing duration distribution by stage"""
    if roster_df.empty:
        return None
    
    # Prepare duration data
    duration_cols = {
        'PRE_PROCESSING_DURATION': 'Pre-Processing',
        'ISF_GEN_DURATION': 'ISF Generation',
        'DART_GEN_DURATION': 'DART Generation',
        'SPS_LOAD_DURATION': 'SPS Load'
    }
    
    duration_data = []
    for col, label in duration_cols.items():
        if col in roster_df.columns:
            valid_durations = roster_df[roster_df[col] > 0][col]
            for duration in valid_durations:
                duration_data.append({'Stage': label, 'Duration (min)': duration})
    
    if not duration_data:
        return None
    
    df_duration = pd.DataFrame(duration_data)
    
    fig = px.box(
        df_duration,
        x='Stage',
        y='Duration (min)',
        title='Processing Duration Distribution by Stage',
        color='Stage'
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        height=400,
        showlegend=False
    )
    
    return fig


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    # Header
    st.title("📊 Roster Processing Dashboard")
    st.markdown("**Automated Analytics Pipeline** | HiLabs Workshop @ E-Summit IIT Roorkee")
    st.markdown("---")
    
    # Load data
    with st.spinner("Loading data..."):
        agg_df = load_aggregated_metrics()
        roster_df = load_roster_processing_details()
    
    if agg_df.empty and roster_df.empty:
        st.error("❌ No data available. Please ensure CSV files are in the correct location.")
        return
    
    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    
    # Month filter
    if not agg_df.empty and 'MONTH' in agg_df.columns:
        available_months = sorted(agg_df['MONTH'].unique(), reverse=True)
        selected_month = st.sidebar.selectbox(
            "Select Month",
            options=['All'] + list(available_months),
            index=0
        )
        if selected_month == 'All':
            selected_month = None
    else:
        selected_month = None
    
    # Market filter
    if not agg_df.empty and 'MARKET' in agg_df.columns:
        available_markets = ['All'] + sorted(agg_df['MARKET'].unique().tolist())
        selected_market = st.sidebar.selectbox("Select Market", available_markets)
        if selected_market != 'All':
            agg_df = agg_df[agg_df['MARKET'] == selected_market]
    
    # State filter
    if not roster_df.empty and 'CNT_STATE' in roster_df.columns:
        available_states = ['All'] + sorted(roster_df['CNT_STATE'].unique().tolist())
        selected_state = st.sidebar.selectbox("Select State", available_states)
        if selected_state != 'All':
            roster_df = roster_df[roster_df['CNT_STATE'] == selected_state]
    
    st.sidebar.markdown("---")
    st.sidebar.info(
        "💡 **Tip**: Use filters to drill down into specific months, "
        "markets, or states for detailed analysis."
    )
    
    # Compute KPIs
    kpis = compute_kpis(agg_df, roster_df, selected_month)
    
    # Display KPIs
    st.subheader("📈 Key Performance Indicators")
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📊 Total Transactions",
            value=f"{kpis['total_transactions']:,}",
            delta=None
        )
    
    with col2:
        st.metric(
            label="✅ Success Rate",
            value=f"{kpis['success_rate']:.2f}%",
            delta=None
        )
    
    with col3:
        st.metric(
            label="❌ Total Failures",
            value=f"{kpis['total_failures']:,}",
            delta=None
        )
    
    with col4:
        st.metric(
            label="🔄 Reprocess Recovery",
            value=f"{kpis['reprocess_recovery']:,}",
            delta=f"+{kpis['reprocess_recovery']:,}" if kpis['reprocess_recovery'] > 0 else "0"
        )
    
    st.markdown("---")
    
    # Visualizations
    st.subheader("📊 Analytics & Insights")
    
    # Row 1: Monthly trend and First vs Next iteration
    col1, col2 = st.columns(2)
    
    with col1:
        trend_chart = create_monthly_trend(agg_df)
        if trend_chart:
            st.plotly_chart(trend_chart, use_container_width=True)
        else:
            st.info("Monthly trend data not available")
    
    with col2:
        iter_chart = create_first_vs_next_iter(agg_df)
        if iter_chart:
            st.plotly_chart(iter_chart, use_container_width=True)
        else:
            st.info("Iteration comparison data not available")
    
    # Row 2: Processing stages and duration analysis
    st.markdown("---")
    st.subheader("⚙️ Processing Stage Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        stage_chart = create_processing_stage_chart(roster_df)
        if stage_chart:
            st.plotly_chart(stage_chart, use_container_width=True)
        else:
            st.info("Processing stage data not available")
    
    with col2:
        duration_chart = create_duration_analysis(roster_df)
        if duration_chart:
            st.plotly_chart(duration_chart, use_container_width=True)
        else:
            st.info("Duration data not available")
    
    # Row 3: Top failures by different dimensions
    st.markdown("---")
    st.subheader("🔴 Failed Roster Analysis")
    
    tab1, tab2, tab3 = st.tabs(["By State", "By Organization", "By Line of Business"])
    
    with tab1:
        failures_state = create_top_failures_chart(roster_df, 'CNT_STATE', 10)
        if failures_state:
            st.plotly_chart(failures_state, use_container_width=True)
        else:
            st.success("✅ No failed rosters by state")
    
    with tab2:
        failures_org = create_top_failures_chart(roster_df, 'ORG_NM', 10)
        if failures_org:
            st.plotly_chart(failures_org, use_container_width=True)
        else:
            st.success("✅ No failed rosters by organization")
    
    with tab3:
        failures_lob = create_top_failures_chart(roster_df, 'LOB', 10)
        if failures_lob:
            st.plotly_chart(failures_lob, use_container_width=True)
        else:
            st.success("✅ No failed rosters by Line of Business")
    
    # Row 4: Detailed failure table
    st.markdown("---")
    st.subheader("📋 Failed Roster Details")
    
    failure_table = create_failure_details_table(roster_df, limit=50)
    if not failure_table.empty:
        st.dataframe(
            failure_table,
            use_container_width=True,
            height=400,
            hide_index=True
        )
        
        # Download button
        csv = failure_table.to_csv(index=False)
        st.download_button(
            label="⬇️ Download Failed Roster Details (CSV)",
            data=csv,
            file_name=f"failed_rosters_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    else:
        st.success("✅ No failed rosters found in the filtered data!")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        "Built with ❤️ for HiLabs Workshop | E-Summit IIT Roorkee 2026"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
