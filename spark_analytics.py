from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import pandas as pd
import os

class EducationAnalytics:
    def __init__(self):
        # Initialize Spark session for distributed processing
        self.spark = SparkSession.builder \
            .appName("EducationAnalytics") \
            .config("spark.sql.adaptive.enabled", "true") \
            .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
            .getOrCreate()
        
        self.spark.sparkContext.setLogLevel("ERROR")
        print("Spark session initialized for large-scale data processing")
    
    def process_enrollment_data(self):
        """Process enrollment data using PySpark for scalable analytics"""
        
        print("\nEducation Analytics - PySpark Implementation")
        print("=" * 50)
        
        # Define data schema for type safety
        schema = StructType([
            StructField("school_name", StringType(), True),
            StructField("region", StringType(), True),
            StructField("academic_year", IntegerType(), True),
            StructField("grade", StringType(), True),
            StructField("gender", StringType(), True),
            StructField("enrollment_count", IntegerType(), True),
            StructField("performance_score", DoubleType(), True),
            StructField("attendance_rate", DoubleType(), True)
        ])
        
        # Load data with schema validation
        df = self.spark.read.csv("data/raw/school_enrollment.csv", 
                                header=True, schema=schema)
        
        print(f"Loaded {df.count():,} enrollment records for analysis")
        
        # Data quality filtering
        df_clean = df.filter(
            (col("enrollment_count") > 0) &
            (col("performance_score").between(0, 100)) &
            (col("academic_year").between(2020, 2024)) &
            (col("region").isNotNull())
        )
        
        # Standardize data formats
        df_clean = df_clean.withColumn("region", upper(col("region"))) \
                          .withColumn("gender", initcap(col("gender"))) \
                          .withColumn("school_name", initcap(col("school_name")))
        
        # Add performance indicators
        df_clean = df_clean.withColumn("at_risk_student", 
                                      when(col("performance_score") < 70, 1).otherwise(0))
        
        print(f"Data validation completed: {df_clean.count():,} records processed")
        
        # Register for SQL operations
        df_clean.createOrReplaceTempView("enrollment_data")
        
        # Generate enrollment trends using Spark SQL
        trends_query = """
        SELECT 
            academic_year,
            region,
            SUM(enrollment_count) as total_enrollment,
            ROUND(AVG(performance_score), 2) as avg_performance,
            SUM(at_risk_student) as at_risk_students,
            COUNT(DISTINCT school_name) as school_count
        FROM enrollment_data
        GROUP BY academic_year, region
        ORDER BY region, academic_year
        """
        
        trends_df = self.spark.sql(trends_query)
        print("Generated enrollment trends analysis using distributed SQL processing")
        
        # Calculate growth rates using window functions
        from pyspark.sql.window import Window
        
        window_spec = Window.partitionBy("region").orderBy("academic_year")
        trends_with_growth = trends_df.withColumn(
            "growth_rate",
            round(((col("total_enrollment") - lag("total_enrollment").over(window_spec)) / 
                   lag("total_enrollment").over(window_spec) * 100), 2)
        )
        
        # School performance analysis
        school_performance = df_clean.groupBy("school_name", "region") \
                                   .agg(
                                       sum("enrollment_count").alias("total_students"),
                                       avg("performance_score").alias("avg_score"),
                                       avg("attendance_rate").alias("avg_attendance"),
                                       sum("at_risk_student").alias("at_risk_count")
                                   )
        
        # Performance classification
        school_performance = school_performance.withColumn(
            "performance_category",
            when(col("avg_score") >= 85, "Excellent")
            .when(col("avg_score") >= 70, "Satisfactory")
            .otherwise("Needs Improvement")
        )
        
        print("Completed school performance analysis with distributed aggregations")
        
        # Display sample results
        print("\nSample Enrollment Trends:")
        trends_with_growth.show(5, truncate=False)
        
        print("\nTop Performing Schools:")
        school_performance.orderBy(desc("avg_score")).show(5, truncate=False)
        
        # Convert to pandas for output (Windows compatibility)
        print("\nExporting results for dashboard integration...")
        
        trends_pandas = trends_with_growth.toPandas()
        performance_pandas = school_performance.toPandas()
        
        # Save results
        os.makedirs("spark_analytics", exist_ok=True)
        trends_pandas.to_csv("spark_analytics/enrollment_trends_spark.csv", index=False)
        performance_pandas.to_csv("spark_analytics/school_performance_spark.csv", index=False)
        
        print(f"Spark analytics completed:")
        print(f"- Enrollment trends: {len(trends_pandas)} records")
        print(f"- School performance: {len(performance_pandas)} schools")
        
        return {
            'trends': trends_pandas,
            'performance': performance_pandas,
            'total_records': df.count(),
            'clean_records': df_clean.count()
        }
    
    def stop_spark(self):
        """Clean up Spark resources"""
        self.spark.stop()
        print("Spark session terminated")

def run_spark_analytics():
    """Execute PySpark analytics for education data"""
    
    analytics = EducationAnalytics()
    
    try:
        results = analytics.process_enrollment_data()
        
        print(f"\nPySpark Analytics Summary:")
        print(f"Total records processed: {results['total_records']:,}")
        print(f"Valid records analyzed: {results['clean_records']:,}")
        print(f"Analytics datasets created: 2")
        print("Results exported for dashboard visualization")
        
        return True
        
    except Exception as e:
        print(f"Analytics processing failed: {str(e)}")
        return False
    finally:
        analytics.stop_spark()

if __name__ == "__main__":
    run_spark_analytics()