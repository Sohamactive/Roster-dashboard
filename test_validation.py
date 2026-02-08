"""
Quick validation test for Roster Dashboard
Tests data loading and basic metric computation
"""

import pandas as pd
import sys

def test_data_loading():
    """Test that CSV files can be loaded"""
    print("Testing data loading...")
    
    # Test roster_processing_details.csv
    try:
        roster_df = pd.read_csv('roster_processing_details.csv')
        print(f"✅ Loaded roster_processing_details.csv: {len(roster_df)} rows")
    except Exception as e:
        print(f"❌ Error loading roster_processing_details.csv: {e}")
        return False
    
    # Test aggregated_operational_metrics.csv
    try:
        agg_df = pd.read_csv('aggregated_operational_metrics.csv')
        print(f"✅ Loaded aggregated_operational_metrics.csv: {len(agg_df)} rows")
    except Exception as e:
        print(f"❌ Error loading aggregated_operational_metrics.csv: {e}")
        return False
    
    return True, roster_df, agg_df


def test_data_integrity(roster_df, agg_df):
    """Test basic data integrity"""
    print("\nTesting data integrity...")
    
    # Check required columns in roster_df
    required_roster_cols = ['ORG_NM', 'CNT_STATE', 'IS_FAILED', 'RUN_NO']
    missing_cols = [col for col in required_roster_cols if col not in roster_df.columns]
    if missing_cols:
        print(f"❌ Missing columns in roster data: {missing_cols}")
        return False
    print(f"✅ All required roster columns present")
    
    # Check required columns in agg_df
    required_agg_cols = ['MONTH', 'MARKET', 'OVERALL_SCS_CNT', 'OVERALL_FAIL_CNT']
    missing_cols = [col for col in required_agg_cols if col not in agg_df.columns]
    if missing_cols:
        print(f"❌ Missing columns in aggregated data: {missing_cols}")
        return False
    print(f"✅ All required aggregated columns present")
    
    # Check for failed rosters
    failed_count = (roster_df['IS_FAILED'] == 1).sum()
    print(f"ℹ️  Found {failed_count} failed rosters")
    
    return True


def test_metrics_computation(agg_df):
    """Test KPI computations"""
    print("\nTesting metrics computation...")
    
    # Compute basic metrics
    total_success = agg_df['OVERALL_SCS_CNT'].sum()
    total_failures = agg_df['OVERALL_FAIL_CNT'].sum()
    total_transactions = total_success + total_failures
    success_rate = (total_success / total_transactions * 100) if total_transactions > 0 else 0
    
    print(f"📊 Total Transactions: {total_transactions:,}")
    print(f"📊 Total Success: {total_success:,}")
    print(f"📊 Total Failures: {total_failures:,}")
    print(f"📊 Success Rate: {success_rate:.2f}%")
    
    if total_transactions > 0:
        print("✅ Metrics computed successfully")
        return True
    else:
        print("❌ No data to compute metrics")
        return False


def main():
    print("=" * 60)
    print("Roster Dashboard Validation Test")
    print("=" * 60)
    print()
    
    # Test 1: Data Loading
    result = test_data_loading()
    if not result:
        print("\n❌ Data loading test failed!")
        sys.exit(1)
    
    _, roster_df, agg_df = result
    
    # Test 2: Data Integrity
    if not test_data_integrity(roster_df, agg_df):
        print("\n❌ Data integrity test failed!")
        sys.exit(1)
    
    # Test 3: Metrics Computation
    if not test_metrics_computation(agg_df):
        print("\n❌ Metrics computation test failed!")
        sys.exit(1)
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ All validation tests passed!")
    print("=" * 60)
    print("\nYou can now run the dashboard:")
    print("  streamlit run app.py")
    print()


if __name__ == "__main__":
    main()
