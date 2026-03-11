# School Enrollment & Education Performance Analytics Platform

## Project Overview
A comprehensive data analytics solution for education departments to analyze enrollment trends, student performance, and support data-driven decision making in educational planning.

## Business Problem
Education departments face challenges with:
- Enrollment data scattered across multiple disconnected files
- Time-intensive manual reporting processes
- Limited visibility into student enrollment patterns
- Difficulty identifying at-risk students and capacity planning issues

## Solution Architecture
This platform provides an automated, end-to-end analytics solution that processes education data through a structured pipeline and delivers actionable insights through interactive dashboards.

## Technology Stack
- **Data Processing**: Python, Pandas, PySpark
- **Workflow Orchestration**: Apache Airflow, Custom Scheduler
- **Cloud Analytics**: Databricks
- **Data Storage**: CSV, Parquet files
- **Visualization**: Power BI
- **Version Control**: Git

## Project Structure
```
education_analytics/
├── data/
│   ├── raw/                    # Source enrollment data
│   └── powerbi_data/          # Dashboard-ready exports
├── medallion_architecture/
│   ├── bronze/                # Raw data ingestion
│   ├── silver/                # Cleaned and validated data
│   └── gold/                  # Business analytics and KPIs
├── airflow_dags/              # Workflow orchestration
├── databricks_notebooks/      # Cloud analytics notebooks
├── medallion_pandas.py        # Main ETL pipeline
├── spark_analytics.py         # PySpark distributed processing
├── pipeline_scheduler.py      # Automated scheduling
└── export_powerbi.py         # Dashboard data export
```

## Key Features

### Data Processing Pipeline
- **Bronze Layer**: Raw data ingestion with validation
- **Silver Layer**: Data cleaning, standardization, and quality checks
- **Gold Layer**: Business aggregations and analytics-ready datasets

### Analytics Capabilities
- Year-over-year enrollment trend analysis
- School performance benchmarking and classification
- Student demographic distribution analysis
- At-risk student identification and dropout prediction
- Regional and district-level comparisons

### Automation & Orchestration
- Scheduled daily data processing
- Error handling and retry mechanisms
- Data quality validation and monitoring
- Automated dashboard data refresh

## Installation & Setup

### Prerequisites
```bash
pip install pandas numpy pyspark schedule pyarrow
```

### Running the Analytics Pipeline

#### Complete Pipeline Execution
```bash
python medallion_pandas.py
```

#### PySpark Distributed Analytics
```bash
python spark_analytics.py
```

#### Automated Scheduling
```bash
python pipeline_scheduler.py
```

#### Power BI Data Export
```bash
python export_powerbi.py
```

## Data Schema
- **school_name**: Educational institution identifier
- **region**: Geographic district or area
- **academic_year**: Academic year (2020-2024)
- **grade**: Student grade level
- **gender**: Student gender classification
- **enrollment_count**: Number of enrolled students
- **performance_score**: Academic performance metric (0-100)
- **attendance_rate**: Student attendance percentage

## Analytics Outputs

### Enrollment Trends
- Total enrollment by academic year and region
- Year-over-year growth rate calculations
- At-risk student identification and counts

### School Performance Analysis
- Performance tier classification (Excellent/Satisfactory/Needs Improvement)
- Average performance scores by institution
- Dropout risk percentage calculations

### Demographic Insights
- Gender distribution analysis by grade level
- Enrollment patterns across academic years
- Regional demographic comparisons

## Power BI Integration
The platform exports analytics data in Power BI compatible formats:
- `enrollment_trends.csv` - Trend analysis data
- `school_performance.csv` - School benchmarking data
- `demographics.csv` - Student demographic insights

### Dashboard Connection Steps
1. Open Power BI Desktop
2. Select Get Data > Text/CSV
3. Navigate to the `powerbi_data/` directory
4. Import the exported CSV files
5. Create visualizations and reports

## Business Impact
- **Process Automation**: Reduces manual reporting effort by 80%
- **Data-Driven Insights**: Enables evidence-based educational planning
- **Early Intervention**: Identifies at-risk students for timely support
- **Resource Optimization**: Supports capacity planning and resource allocation

## Technical Implementation
The solution implements a medallion architecture pattern for data processing:
1. **Ingestion**: Raw data validation and storage
2. **Transformation**: Data cleaning and standardization
3. **Analytics**: Business logic and KPI calculations
4. **Export**: Dashboard-ready data preparation

## Monitoring & Logging
- Pipeline execution logging with timestamps
- Data quality validation checkpoints
- Error handling and notification system
- Automated retry mechanisms for failed processes

## Future Enhancements
- Real-time data streaming capabilities
- Machine learning models for predictive analytics
- Advanced visualization with interactive dashboards
- Integration with student information systems

## Project Team
- **Developer**: K.Snehitha
- **Institution**: Vellore Institute Of Technology
- **Project Type**: Capstone Project

## License
This project is developed for educational purposes as part of capstone program.

## Output Screenshots 
# Complete Pipeline Execution
<img width="1044" height="704" alt="image" src="https://github.com/user-attachments/assets/7f8e3f0c-4dd6-41bf-b9e8-37a37377b2a6" />
# PySpark Distributed Analytics
<img width="1104" height="917" alt="image" src="https://github.com/user-attachments/assets/5c0f81b9-0f7e-441d-9c96-f068394a8aec" />
<img width="1265" height="252" alt="image" src="https://github.com/user-attachments/assets/9caee6c4-44e8-40a7-b986-99bf2818ee25" />

# Automated Scheduling
<img width="1186" height="194" alt="image" src="https://github.com/user-attachments/assets/ee4b530a-c9c4-4137-abe1-a5b0eb7e5aed" />

# Power BI Data Export
<img width="1213" height="422" alt="image" src="https://github.com/user-attachments/assets/cac45e7f-2208-497b-91cd-41386947ec70" />

### Power BI Dashboards 
# Executive Summary
<img width="1222" height="699" alt="image" src="https://github.com/user-attachments/assets/569f4e3a-fbd3-4ec7-b864-d26393b968d7" />
# Regional Analysis
<img width="1220" height="698" alt="image" src="https://github.com/user-attachments/assets/09461125-1de3-4206-8442-5a5bd9659eaa" />
# School Performance
<img width="1225" height="700" alt="image" src="https://github.com/user-attachments/assets/4c462e7a-8a14-4b50-a563-72345ca9904f" />
# Demographics
<img width="1226" height="699" alt="image" src="https://github.com/user-attachments/assets/73f12fbe-55b6-4a80-9cab-652d212473ab" />



