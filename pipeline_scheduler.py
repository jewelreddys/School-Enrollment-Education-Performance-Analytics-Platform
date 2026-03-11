import schedule
import time
import subprocess
import sys
from datetime import datetime
import logging

# Configure logging for pipeline monitoring
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pipeline_execution.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def execute_data_pipeline():
    """Execute the education analytics data pipeline"""
    logger.info("Starting scheduled data pipeline execution")
    
    try:
        # Run the main data processing pipeline
        result = subprocess.run([sys.executable, "medallion_pandas.py"], 
                              capture_output=True, text=True, cwd=".")
        
        if result.returncode == 0:
            logger.info("Data pipeline executed successfully")
            logger.info("Analytics data updated and ready for reporting")
        else:
            logger.error("Data pipeline execution failed")
            logger.error(result.stderr)
            
    except Exception as e:
        logger.error(f"Pipeline execution error: {e}")

def start_pipeline_scheduler():
    """Start the automated pipeline scheduler"""
    # Schedule daily execution at 6:00 AM
    schedule.every().day.at("06:00").do(execute_data_pipeline)
    
    logger.info("Education Analytics Pipeline Scheduler Started")
    logger.info("Scheduled for daily execution at 6:00 AM")
    logger.info("Press Ctrl+C to stop the scheduler")
    
    # Execute pipeline once immediately for testing
    execute_data_pipeline()
    
    # Keep scheduler running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    try:
        start_pipeline_scheduler()
    except KeyboardInterrupt:
        logger.info("Pipeline scheduler stopped by user")
    except Exception as e:
        logger.error(f"Scheduler error: {e}")