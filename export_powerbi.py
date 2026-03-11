import pandas as pd
import os
from pathlib import Path

def export_analytics_for_powerbi():
    """Export processed analytics data for Power BI dashboard integration"""
    
    print("Power BI Data Export Utility")
    print("=" * 35)
    
    # Create export directory
    export_dir = Path("powerbi_data")
    export_dir.mkdir(exist_ok=True)
    
    # Define source files from Gold layer
    source_files = {
        'enrollment_trends': 'medallion_architecture/gold/enrollment_trends.parquet',
        'school_performance': 'medallion_architecture/gold/school_performance.parquet',
        'demographics': 'medallion_architecture/gold/demographics.parquet'
    }
    
    exported_files = []
    
    print("Converting analytics data to Power BI compatible format...")
    
    for dataset_name, source_path in source_files.items():
        if os.path.exists(source_path):
            # Read Parquet file
            df = pd.read_parquet(source_path)
            
            # Export as CSV for Power BI
            export_path = export_dir / f"{dataset_name}.csv"
            df.to_csv(export_path, index=False)
            
            print(f"Exported {dataset_name}: {len(df):,} records")
            exported_files.append(str(export_path))
        else:
            print(f"Warning: {dataset_name} source file not found")
    
    if exported_files:
        print(f"\nExport completed successfully!")
        print(f"Files ready for Power BI import:")
        for file_path in exported_files:
            print(f"  - {file_path}")
        
        print(f"\nPower BI Connection Instructions:")
        print(f"1. Open Power BI Desktop")
        print(f"2. Get Data > Text/CSV")
        print(f"3. Navigate to: {export_dir.absolute()}")
        print(f"4. Import the CSV files for dashboard creation")
    else:
        print("No data files were exported. Please run the main pipeline first.")
    
    return len(exported_files)

if __name__ == "__main__":
    export_analytics_for_powerbi()