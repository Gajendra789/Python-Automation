import pandas as pd
import logging
import os
import time
from logging.handlers import RotatingFileHandler
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# Configure logging with rotating file handler to manage log file size
log_handler = RotatingFileHandler('etl_process.log', maxBytes=5*1024*1024, backupCount=3)  # 5MB per log file, keep 3 backups
logging.basicConfig(handlers=[log_handler], level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# File to store the last processed timestamp
LAST_PROCESSED_FILE = 'last_processed.txt'

# Function to read the last processed timestamp
def read_last_processed():
    if os.path.exists(LAST_PROCESSED_FILE):
        with open(LAST_PROCESSED_FILE, 'r') as file:
            return file.read().strip()
    return None

# Function to write the last processed timestamp
def write_last_processed(timestamp):
    with open(LAST_PROCESSED_FILE, 'w') as file:
        file.write(timestamp)

# -------------------
# Step 1: Extract
# -------------------
# Read data from a CSV file
def extract_data(file_path, last_processed):
    try:
        logging.info(f"Extracting data from {file_path}...")
        df = pd.read_csv(file_path)
        if last_processed:
            df['OrderDate'] = pd.to_datetime(df['OrderDate'], errors='coerce')
            df = df[df['OrderDate'] > pd.to_datetime(last_processed)]
        # Filter out rows with invalid 'OrderDate' after coercion
        df = df.dropna(subset=['OrderDate'])
        logging.info(f"Data extracted. {len(df)} records loaded.")
        return df
    except FileNotFoundError:
        logging.error(f"Error: The file {file_path} was not found.")
    except pd.errors.EmptyDataError:
        logging.error("Error: The file is empty")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    return None

# -------------------
# Step 2: Transform
# -------------------
# Function to clean and transform data
def transform_data(df):
    try:
        logging.info("Transforming data...")
        if 'Amount' in df.columns:
            # 1. Handle missing values (example: fill NaN values in 'Amount' with 0)
            df['Amount'].fillna(0, inplace=True)

        if 'OrderDate' in df.columns:
            # 2. Convert data types (example: ensure 'OrderDate' is a datetime)
            df['OrderDate'] = pd.to_datetime(df['OrderDate'], errors='coerce')

        # 3. Create new columns (example: adding 'Year' and 'Month' from 'OrderDate')
        df['Year'] = df['OrderDate'].dt.year
        df['Month'] = df['OrderDate'].dt.month

        # 4. Aggregate data (example: Total sales per region)
        if 'Region' in df.columns:
            sales_per_region = df.groupby('Region')['Amount'].sum().reset_index()
            logging.info("Sales per region:")
            logging.info(sales_per_region)

        # 5. Drop unnecessary columns (example: 'Region' if not needed)
        df = df.drop(columns=['Region'], errors='ignore')  # Use `errors='ignore'` to avoid issues if column is missing

        # 6. Filter data (example: only include orders above 100)
        df = df[df['Amount'] > 100]
        logging.info(f"Data transformed. {len(df)} records after transformation.")
        return df
    except KeyError as e:
        logging.error(f"Error: Missing column in data - {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred during transformation: {e}")
    return None

# -------------------
# Step 3: Load
# -------------------
# Function to load data into a new CSV file
def load_data(df, output_path):
    try:
        logging.info(f"Loading data into {output_path}...")
        df.to_csv(output_path, index=False, mode='a', header=not os.path.exists(output_path))
        logging.info(f"Data successfully loaded into {output_path}.")
    except Exception as e:
        logging.error(f"An unexpected error occurred during loading: {e}")

# -------------------
# Full ETL Process
# -------------------
def etl_process(input_file, output_file):
    last_processed = read_last_processed()
    
    # Extract
    data = extract_data(input_file, last_processed)
    if data is not None and not data.empty:
        # Transform
        transformed_data = transform_data(data)
        if transformed_data is not None:
            # Load
            load_data(transformed_data, output_file)
            # Update the last processed timestamp
            latest_timestamp = transformed_data['OrderDate'].max().strftime('%Y-%m-%d %H:%M:%S')
            write_last_processed(latest_timestamp)

# Function to process multiple files concurrently using ThreadPoolExecutor
def process_multiple_files(input_files, output_file):
    with ThreadPoolExecutor() as executor:
        executor.map(lambda input_file: etl_process(input_file, output_file), input_files)

# Example usage
if __name__ == "__main__":
    input_files = ['data1.csv', 'data2.csv']  # Modify with actual file paths
    output_file = 'output.csv'  # Modify with the desired output file path
    process_multiple_files(input_files, output_file)
