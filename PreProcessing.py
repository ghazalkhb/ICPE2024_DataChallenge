import pandas as pd

# Loop through file numbers 0 to 19
for i in range(20):
    file_path = f'[folder path]/CallGraph_{i}.csv'
    dataframe = pd.read_csv(file_path, on_bad_lines='warn')
    
    # Rename columns
    dataframe = dataframe[['um', 'dm', 'timestamp', 'service', 'traceid']]
    dataframe.columns = ['source', 'target', 'timestamp', 'service', 'traceid']
    
    # Write modified dataframe to CSV
    output_file_path = f'[folder path]/CallGraph__sorted{i}.csv'
    dataframe.to_csv(output_file_path, index=False)

