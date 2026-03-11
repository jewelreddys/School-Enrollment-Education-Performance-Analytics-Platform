#!/usr/bin/env python3
"""
PySpark + Power BI Pipeline Setup and Execution Script
Run this to set up PySpark and process education data for Power BI
"""

import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """Install required packages for PySpark processing"""
    print("📦 Installing PySpark and dependencies...")
    
    packages = [
        "pyspark==3.5.0",
        "findspark",
        "pandas",
        "numpy"
    ]
    
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ Installed {package}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")
            return False
    
    return True

def setup_environment():
    """Set up PySpark environment variables"""
    print("🔧 Setting up PySpark environment...")
    
    # Set environment variables
    os.environ['PYSPARK_PYTHON'] = sys.executable
    os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable
    
    # Initialize findspark
    try:
        import findspark
        findspark.init()
        print("✅ PySpark environment configured")
        return True
    except ImportError:
        print("❌ Failed to configure PySpark environment")
        return False

def create_directories():
    """Create necessary directories"""
    print("📁 Creating project directories...")
    
    directories = [
        "data/raw",
        "data/processed", 
        "data/analytics",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created {directory}")

def run_data_generation():
    """Generate sample data if raw data doesn't exist"""
    raw_data_path = Path("data/raw/school_enrollment.csv")
    
    if not raw_data_path.exists():
        print("📊 Generating sample education data...")
        try:
            subprocess.run([sys.executable, "scripts/generate_sample_data.py"], check=True)
            print("✅ Sample data generated")
        except subprocess.CalledProcessError:
            print("❌ Failed to generate sample data")
            return False
    else:
        print("✅ Raw data already exists")
    
    return True

def run_pyspark_processing():
    """Run PySpark analytics processing"""
    print("⚡ Running PySpark analytics processing...")
    
    try:
        subprocess.run([sys.executable, "src/spark_processing/education_analytics.py"], check=True)
        print("✅ PySpark processing completed")
        return True
    except subprocess.CalledProcessError:
        print("❌ PySpark processing failed")
        return False

def validate_output_files():
    """Validate that all required files for Power BI are created"""
    print("🔍 Validating output files for Power BI...")
    
    required_files = [
        "data/analytics/enrollment_trends.csv",
        "data/analytics/school_performance.csv",
        "data/analytics/demographics.csv",
        "data/processed/enrollment_clean.csv"
    ]
    
    all_files_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            file_size = Path(file_path).stat().st_size
            print(f"✅ {file_path} ({file_size:,} bytes)")
        else:
            print(f"❌ Missing: {file_path}")
            all_files_exist = False
    
    return all_files_exist

def display_next_steps():
    """Display next steps for Power BI implementation"""
    print("\n" + "="*60)
    print("🎯 PYSPARK PROCESSING COMPLETED SUCCESSFULLY!")
    print("="*60)
    
    print("\n📊 Files ready for Power BI:")
    print("   → data/analytics/enrollment_trends.csv")
    print("   → data/analytics/school_performance.csv")
    print("   → data/analytics/demographics.csv")
    print("   → data/processed/enrollment_clean.csv")
    
    print("\n📈 Next Steps:")
    print("1. Open Power BI Desktop")
    print("2. Follow the Power BI implementation guide:")
    print("   → dashboards/PowerBI_Ultra_Clear_Guide.md")
    print("3. Import the 4 CSV files using Get Data → Text/CSV")
    print("4. Build your 4-page education analytics dashboard")
    
    print("\n🚀 Power BI Import Commands:")
    print("   Get Data → Text/CSV → Select files above")
    print("   Create relationships and measures as per guide")
    
    print("\n⏱️  Estimated Power BI setup time: 90 minutes")
    print("🎉 You'll have a complete education analytics solution!")

def main():
    """Main pipeline execution"""
    print("🚀 EDUCATION ANALYTICS PIPELINE SETUP")
    print("="*50)
    
    # Step 1: Install requirements
    if not install_requirements():
        print("❌ Failed to install requirements")
        return False
    
    # Step 2: Setup environment
    if not setup_environment():
        print("❌ Failed to setup environment")
        return False
    
    # Step 3: Create directories
    create_directories()
    
    # Step 4: Generate sample data
    if not run_data_generation():
        print("❌ Failed to generate data")
        return False
    
    # Step 5: Run PySpark processing
    if not run_pyspark_processing():
        print("❌ Failed PySpark processing")
        return False
    
    # Step 6: Validate outputs
    if not validate_output_files():
        print("❌ Output validation failed")
        return False
    
    # Step 7: Display next steps
    display_next_steps()
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ Setup completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Setup failed!")
        sys.exit(1)