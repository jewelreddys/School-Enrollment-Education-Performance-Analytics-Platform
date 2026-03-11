import pandas as pd
import os
from pathlib import Path

def ingest_to_bronze():
    """Bronze Layer: Raw CSV to structured storage"""
    print("Initiating data ingestion process...")
    
    # Create bronze directory
    Path("medallion_architecture/bronze").mkdir(parents=True, exist_ok=True)
    
    # Read raw CSV
    df = pd.read_csv("data/raw/school_enrollment.csv")
    
    # Save to Bronze layer in Parquet format for better performance
    df.to_parquet("medallion_architecture/bronze/enrollment_data.parquet", index=False)
    
    print(f"Data ingestion completed successfully. Processed {len(df)} enrollment records.")
    return df

def transform_to_silver():
    """Silver Layer: Data cleaning and validation"""
    print("Performing data cleaning and validation...")
    
    # Create silver directory
    Path("medallion_architecture/silver").mkdir(parents=True, exist_ok=True)
    
    # Read from Bronze layer
    df = pd.read_parquet("medallion_architecture/bronze/enrollment_data.parquet")
    
    # Apply data quality filters
    df_clean = df[
        (df['enrollment_count'] > 0) &
        (df['performance_score'].between(0, 100)) &
        (df['academic_year'].between(2020, 2024)) &
        (df['region'].notna()) &
        (df['school_name'].notna())
    ].copy()
    
    # Standardize text fields for consistency
    df_clean['region'] = df_clean['region'].str.upper()
    df_clean['gender'] = df_clean['gender'].str.title()
    df_clean['school_name'] = df_clean['school_name'].str.title()
    
    # Add performance indicators
    df_clean['is_high_performer'] = df_clean['performance_score'] >= 85
    
    # Save cleaned data to Silver layer
    df_clean.to_parquet("medallion_architecture/silver/enrollment_clean.parquet", index=False)
    
    print(f"Data cleaning completed. {len(df_clean)} validated records ready for analysis.")
    return df_clean

def create_gold_analytics():
    """Gold Layer: Business aggregations and analytics"""
    print("Generating business analytics and insights...")
    
    # Create gold directory
    Path("medallion_architecture/gold").mkdir(parents=True, exist_ok=True)
    
    # Read cleaned data from Silver layer
    df = pd.read_parquet("medallion_architecture/silver/enrollment_clean.parquet")
    
    # Create dropout risk indicators
    df['dropout_risk_flag'] = (df['performance_score'] < 70).astype(int)
    
    # Generate enrollment trends analysis
    trends = df.groupby(['academic_year', 'region']).agg({
        'enrollment_count': 'sum',
        'performance_score': 'mean',
        'dropout_risk_flag': 'sum'
    }).reset_index()
    
    trends.columns = ['academic_year', 'region', 'total_enrollment', 'avg_performance', 'high_risk_students']
    
    # Calculate year-over-year growth rates
    trends['growth_rate'] = trends.groupby('region')['total_enrollment'].pct_change() * 100
    trends['growth_rate'] = trends['growth_rate'].round(2)
    
    trends.to_parquet("medallion_architecture/gold/enrollment_trends.parquet", index=False)
    
    # Generate school performance analysis
    performance = df.groupby(['school_name', 'region']).agg({
        'enrollment_count': 'sum',
        'performance_score': 'mean',
        'dropout_risk_flag': 'sum'
    }).reset_index()
    
    performance.columns = ['school_name', 'region', 'total_students', 'avg_score', 'high_risk_count']
    performance['dropout_risk_pct'] = (performance['high_risk_count'] / performance['total_students'] * 100).round(2)
    
    # Classify schools by performance tiers
    performance['performance_tier'] = pd.cut(
        performance['avg_score'], 
        bins=[0, 70, 85, 100], 
        labels=['Needs Improvement', 'Satisfactory', 'Excellent']
    )
    
    performance.to_parquet("medallion_architecture/gold/school_performance.parquet", index=False)
    
    # Generate demographic analysis
    demographics = df.groupby(['academic_year', 'grade', 'gender']).agg({
        'enrollment_count': 'sum'
    }).reset_index()
    
    demographics.columns = ['academic_year', 'grade', 'gender', 'student_count']
    
    # Calculate gender distribution percentages
    total_by_year_grade = demographics.groupby(['academic_year', 'grade'])['student_count'].transform('sum')
    demographics['gender_percentage'] = (demographics['student_count'] / total_by_year_grade * 100).round(2)
    
    demographics.to_parquet("medallion_architecture/gold/demographics.parquet", index=False)
    
    print("Analytics generation completed. Created enrollment trends, school performance, and demographic reports.")
    
    return {
        'trends': trends,
        'performance': performance, 
        'demographics': demographics
    }

def run_medallion_pipeline():
    """Execute the complete Education Analytics ETL pipeline"""
    try:
        print("Education Analytics Platform - Data Processing Pipeline")
        print("=" * 55)
        
        # Execute Bronze Layer processing
        bronze_df = ingest_to_bronze()
        
        # Execute Silver Layer processing
        silver_df = transform_to_silver()
        
        # Execute Gold Layer processing
        gold_tables = create_gold_analytics()
        
        print("\nPipeline Execution Summary")
        print("-" * 30)
        print(f"Raw data processed: {len(bronze_df):,} records")
        print(f"Clean data validated: {len(silver_df):,} records")
        print(f"Analytics reports generated: {len(gold_tables)} datasets")
        
        # Verify output files
        output_files = [
            "medallion_architecture/bronze/enrollment_data.parquet",
            "medallion_architecture/silver/enrollment_clean.parquet",
            "medallion_architecture/gold/enrollment_trends.parquet",
            "medallion_architecture/gold/school_performance.parquet",
            "medallion_architecture/gold/demographics.parquet"
        ]
        
        print("\nOutput Verification")
        print("-" * 20)
        all_files_created = True
        for file_path in output_files:
            if os.path.exists(file_path):
                print(f"Created: {os.path.basename(file_path)}")
            else:
                print(f"Missing: {os.path.basename(file_path)}")
                all_files_created = False
        
        if all_files_created:
            print("\nPipeline execution completed successfully.")
            print("Analytics data is ready for dashboard visualization.")
        else:
            print("\nPipeline completed with some missing outputs.")
        
        return all_files_created
        
    except Exception as e:
        print(f"\nPipeline execution failed: {str(e)}")
        return False

if __name__ == "__main__":
    run_medallion_pipeline()