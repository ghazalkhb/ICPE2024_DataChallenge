import pandas as pd

# Loop through file numbers 0 to 19
for i in range(20):
    # Generate file path
    file_path = f'/home/morteza/Desktop/Alireza/Dataset/data/CallGraph/data/CallGraph_{i}.csv'
    
    # Read CSV file
    dataframe = pd.read_csv(file_path, on_bad_lines='warn')
    
    # Sort dataframe by timestamp
    dataframe = dataframe.sort_values(by=['timestamp'])
    
    # Calculate average rt and fill NaN values
    average_rt = dataframe['rt'].mean()
    dataframe['rt'].fillna(average_rt, inplace=True)
    
    # Rename columns
    dataframe = dataframe[['um', 'dm', 'timestamp', 'service', 'traceid']]
    dataframe.columns = ['source', 'target', 'timestamp', 'service', 'traceid']
    
    # Write modified dataframe to CSV
    output_file_path = f'/home/morteza/Desktop/Alireza/Dataset/data/CallGraph/data/CallGraph__sorted{i}.csv'
    dataframe.to_csv(output_file_path, index=False)

