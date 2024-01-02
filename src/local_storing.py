import os
def save_file(frequency, report_data):
    # Define the directory path
    your_directory_path = os.getcwd()  # Replace with your actual directory path

    # Create the report folder if it doesn't exist
    report_folder = f'reports\\{frequency}'
    report_folder_path = os.path.join(your_directory_path, report_folder)
    if not os.path.exists(report_folder_path):
        os.makedirs(report_folder_path)

     # Save the DataFrames as CSV files in the report folder
    tickers = report_data.index.get_level_values(0).drop_duplicates()
    for key in tickers:
        file_path = os.path.join(report_folder_path, f'{key}.csv')
        report_data.loc[(key),:].reset_index().to_csv(file_path, index=False)

    # # Save the DataFrames as CSV files in the report folder
    # for key in report_data.keys():
    #     file_path = os.path.join(report_folder_path, f'{key}.csv')
    #     report_data[key].reset_index().to_csv(file_path, index=False)