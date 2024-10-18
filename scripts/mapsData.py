import pandas as pd
import os
def get_static_dynamic_file_path(DataType,filename):
    # Get the current script's directory
    script_dir = os.path.dirname(__file__)
    
    # Construct the relative path to the file in the 'static' folder inside 'data'
    file_path = os.path.join(script_dir, '..', 'data', DataType, filename)
    
    # Normalize the path
    return os.path.abspath(file_path)
def get_lat_long(country_code, csv_file=get_static_dynamic_file_path('static','countries.csv')):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    
    # Filter the DataFrame based on the provided country code
    result = df[df['country_id'] == country_code]
    
    # Check if the country code is found and return latitude and longitude
    if not result.empty:
        lat = result.iloc[0]['lat']
        long = result.iloc[0]['long']
        return lat, long
    else:
        return None
# Load the CSV file
def DataMaps(filename='user_data.csv'):
    file_path = filename
    df = pd.read_csv(file_path)

    # Count the occurrences of each country code
    country_counts = df['country_code'].value_counts()

    # Calculate the total number of entries
    total_entries = len(df)

    # Calculate the percentage for each country code
    country_percentages = (country_counts / total_entries) * 100

    # Convert to a dictionary for easier output
    country_percentage_dict = country_percentages.to_dict()

    # Print the results
    country_codes=[]
    percentages=[]
    lats=[]
    longs=[]
    for country_code, percentage in country_percentage_dict.items():
        country_codes.append(country_code)
        percentages.append(percentage)
        lats.append(get_lat_long(country_code)[0])
        longs.append(get_lat_long(country_code)[1])

    data = {
    'country_id': country_codes,
    'lat': lats,
    'lon': longs,
    'probability': percentages
}
    return(data)

