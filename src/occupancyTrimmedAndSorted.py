import pandas as pd
import numpy as np
import os

def get_hourly_average_for_room(input_csv, output_csv, target_floor_space, chunk_size=250000):
    """
    Processes a large occupancy dataset chunk-by-chunk, filters for a target room,
    calculates the hourly average occupancy count per calendar date, fills in any
    missing hours in the timeline with 0s, and saves the result to a CSV.

    Parameters
    ------------
    input_csv : file pathway
        the path to the raw input dataset for occupancy data (with 9 million rows)

    output_csv : file pathway
        the output path to the filtered .csv file for a specified room
    
    target_floor_space : string
        the floorspace id for a specific room to search for in the input database

    chunk_size : integer
        maximum number of rows processed in each block, utilised to reduce memory usuage; defaults to 250000 rows

    Outputs
    -------
    complete_hourly_df : dataframe
        a dataframe containing the filtered room's average occupancy count per hour
        
    
    """
    print(f"Starting processing for Room/Space: {target_floor_space}...")
    
    # Column definitions matching the source layout
    columns = [
        'sensor_id',
        'floor_space_id',
        'current_status',
        'count',
        'timestamp_record',
        'timestamp_event',
        'occupancy_label'
    ]
    
    filtered_chunks = []
    
    # Step 1: Read chunk-by-chunk to save RAM and filter the target space
    for chunk in pd.read_csv(input_csv, names=columns, header=0, chunksize=chunk_size, on_bad_lines='skip'):
        # Filter for the specific room/space
        subset = chunk[chunk['floor_space_id'] == target_floor_space].copy()
        if not subset.empty:
            # Keep only columns necessary for temporal aggregation
            subset = subset[['timestamp_event', 'count']]
            filtered_chunks.append(subset)
            
    if not filtered_chunks:
        print(f"No records found for floor space ID: {target_floor_space}")
        return None
        
    # Combine all filtered records
    df_filtered = pd.concat(filtered_chunks, ignore_index=True)
    print(f"Filtered {len(df_filtered)} records for target space.")
    
    # Step 2: Convert timestamps and extract temporal grouping targets
    df_filtered['timestamp_event'] = pd.to_datetime(df_filtered['timestamp_event'], errors='coerce')
    df_filtered = df_filtered.dropna(subset=['timestamp_event'])
    
    df_filtered['date'] = df_filtered['timestamp_event'].dt.date
    df_filtered['hour'] = df_filtered['timestamp_event'].dt.hour
    df_filtered['day_of_week'] = df_filtered['timestamp_event'].dt.day_name()
    
    # Step 3: Compute average occupancy grouped by calendar date and hour
    hourly_avg = df_filtered.groupby(['date', 'day_of_week', 'hour'])['count'].mean().reset_index()
    hourly_avg.rename(columns={'count': 'average_occupancy_count'}, inplace=True)
    
    # Step 4: Reconstruct a complete date-hour grid to fill in missing timeline hours with 0s
    unique_dates = hourly_avg['date'].unique()
    hours_grid = list(range(24))
    
    grid = pd.MultiIndex.from_product(
        [unique_dates, hours_grid],
        names=['date', 'hour']
    ).to_frame().reset_index(drop=True)
    
    grid['day_of_week'] = pd.to_datetime(grid['date']).dt.day_name()
    
    # Merge grid with the calculated averages and fill missing values with 0
    complete_hourly_df = pd.merge(grid, hourly_avg, on=['date', 'hour', 'day_of_week'], how='left')
    complete_hourly_df['average_occupancy_count'] = complete_hourly_df['average_occupancy_count'].fillna(0.0)
    
    # Sort chronologically
    complete_hourly_df = complete_hourly_df.sort_values(by=['date', 'hour']).reset_index(drop=True)
    
    # Save output to file
    complete_hourly_df.to_csv(output_csv, index=False)
    print(f"Success! Chronological hourly average dataset saved to: {output_csv}")
    return complete_hourly_df

# --- Demo Execution of the function ---
# Unhashtag to run
# raw_input_path = '/content/5occupancySensor_MayToDec2024_9MRows.csv'
# output_summary_path = '/content/hourly_avg_room_G20.csv'
# target_space = 'cca1ac3e-f81f-4ebb-aa2b-8b0bf3e9e53b' # Building 60 - G20
