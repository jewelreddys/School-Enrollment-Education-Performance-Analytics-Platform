"""
Education Analytics Platform - Demo Script
==========================================

This script demonstrates the complete education analytics pipeline
for the capstone project evaluation.
"""

import subprocess
import sys
import os
from datetime import datetime

def run_demo():
    """Execute complete demo for project evaluation"""
    
    print("School Enrollment & Education Performance Analytics Platform")
    print("=" * 65)
    print(f"Demo executed on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    demo_steps = [
        {
            "step": 1,
            "title": "Data Processing Pipeline (Pandas & ETL)",
            "script": "medallion_pandas.py",
            "description": "Medallion Architecture implementation with Bronze/Silver/Gold layers"
        },
        {
            "step": 2, 
            "title": "Distributed Analytics (PySpark)",
            "script": "spark_analytics.py",
            "description": "Large-scale data processing using Apache Spark"
        },
        {
            "step": 3,
            "title": "Power BI Data Export",
            "script": "export_powerbi.py", 
            "description": "Dashboard-ready data export for visualization"
        }
    ]
    
    results = {}
    
    for demo_step in demo_steps:
        print(f"Step {demo_step['step']}: {demo_step['title']}")
        print(f"Description: {demo_step['description']}")
        print("-" * 50)
        
        try:
            result = subprocess.run([sys.executable, demo_step['script']], 
                                  capture_output=True, text=True, cwd=".")
            
            if result.returncode == 0:
                print(result.stdout)
                results[demo_step['step']] = "Success"
            else:
                print(f"Error in {demo_step['title']}: {result.stderr}")
                results[demo_step['step']] = "Failed"
                
        except Exception as e:
            print(f"Execution error: {str(e)}")
            results[demo_step['step']] = "Error"
        
        print("\n" + "=" * 65 + "\n")
    
    # Demo Summary
    print("DEMO EXECUTION SUMMARY")
    print("=" * 25)
    
    for step_num, status in results.items():
        step_info = demo_steps[step_num - 1]
        status_icon = "[SUCCESS]" if status == "Success" else "[FAILED]"
        print(f"{status_icon} Step {step_num}: {step_info['title']} - {status}")
    
    successful_steps = sum(1 for status in results.values() if status == "Success")
    print(f"\nDemo Results: {successful_steps}/{len(demo_steps)} components executed successfully")
    
    if successful_steps == len(demo_steps):
        print("\nProject demonstration completed successfully!")
        print("All pipeline components are working as expected.")
    else:
        print("\nSome components need attention. Please check the error messages above.")
    
    # Show generated outputs
    print("\nGenerated Outputs:")
    output_dirs = ["medallion_architecture", "spark_analytics", "powerbi_data"]
    
    for output_dir in output_dirs:
        if os.path.exists(output_dir):
            files = os.listdir(output_dir)
            if files:
                print(f"  {output_dir}/: {len(files)} files created")
            else:
                print(f"  {output_dir}/: Directory exists but empty")
        else:
            print(f"  {output_dir}/: Not created")

if __name__ == "__main__":
    run_demo()