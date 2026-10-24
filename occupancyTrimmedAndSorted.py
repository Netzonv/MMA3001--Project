# Trim and filter for occupancy data for Building 60 - G20

import pandas as pd

# Trim number of rows from 9 million to 1.5 million for smaller file size and faster calculation
input_file = '/content/5occupancySensor_MayToDec2024_9MRows.csv'
output_file = '/content/5occupancySensor_MayToDec2024_1.5MRows.csv'
target_rows = 1500000
chunk_size = 100000

print(f"Truncating dataset to the first {target_rows} rows...")

# Initialize variable to track total rows written
rows_written = 0
header_written = False

for chunk in pd.read_csv(input_file, chunksize=chunk_size, on_bad_lines='skip'):
    # Determine how many rows from the current chunk to write
    remaining_rows = target_rows - rows_written
    if remaining_rows <= 0:
        break
        
    if len(chunk) > remaining_rows:
        chunk = chunk.iloc[:remaining_rows]
        
    # Save to file
    chunk.to_csv(output_file, mode='a', index=False, header=not header_written)
    header_written = True
    rows_written += len(chunk)
    print(f"Progress: {rows_written} / {target_rows} rows written...")

# Define explicit, clean column names
columns = [
    'sensor_id',
    'floor_space_id',
    'current_status',
    'count',
    'timestamp_record',
    'timestamp_event',
    'occupancy_label'
]

# Load the truncated dataset
print("Loading dataset...")
occ_df = pd.read_csv(
    '/content/5occupancySensor_MayToDec2024_1.5MRows.csv',
    names=columns,
    header=0
)

# Convert timestamp to datetime
occ_df['timestamp_event'] = pd.to_datetime(occ_df['timestamp_event'], errors='coerce')

# Extract temporal features
occ_df['day_of_week'] = occ_df['timestamp_event'].dt.day_name()
occ_df['day_of_week_num'] = occ_df['timestamp_event'].dt.dayofweek
occ_df['hour'] = occ_df['timestamp_event'].dt.hour
occ_df['is_weekend'] = occ_df['day_of_week_num'].isin([5, 6]).astype(int)

# Filter for Building 60 G20 floor space ID in the 2nd column
target_floor_space = 'cca1ac3e-f81f-4ebb-aa2b-8b0bf3e9e53b'
filtered_df = occ_df[occ_df['floor_space_id'] == target_floor_space]

print(f"\n=== Filtered Results for floor_space_id: {target_floor_space} ===")
print(f"Total records found: {len(filtered_df)}")

# Print trimmed dataset, otherwise record invalid result
if len(filtered_df) > 0:
    display(filtered_df[['sensor_id', 'floor_space_id', 'timestamp_event', 'day_of_week', 'hour', 'occupancy_label']].head(10))
    
    print("\n=== Occupancy Label Distribution for this space ===")
    display(filtered_df['occupancy_label'].value_counts())
else:
    print("No records found matching this floor space ID in the first 1.5M rows.")

#Filter for the first 2 weeks



# Load the 2-week subset
two_week_file = '/content/occupancy_first_2_weeks_cca1ac3e.csv'
df_2w = pd.read_csv(two_week_file)

# Ensure the timestamp is in datetime format
df_2w['timestamp_event'] = pd.to_datetime(df_2w['timestamp_event'])

# Extract the actual calendar date (YYYY-MM-DD)
df_2w['date'] = df_2w['timestamp_event'].dt.date

# Group by the specific date, day of week, and hour, then calculate average occupancy count
hourly_daily_specific_avg = df_2w.groupby(['date', 'day_of_week', 'hour'])['count'].mean().reset_index()

# Sort chronologically by date and hour
hourly_daily_specific_avg = hourly_daily_specific_avg.sort_values(by=['date', 'hour'])

# Rename columns for clarity
hourly_daily_specific_avg.rename(columns={
    'count': 'average_occupancy_count'
}, inplace=True)

# Save this specific daily breakdown to a CSV dataset
specific_summary_path = '/content/hourly_avg_per_specific_day.csv'
hourly_daily_specific_avg.to_csv(specific_summary_path, index=False)
print(f"Successfully saved specific daily-hourly averages dataset to: {specific_summary_path}")


