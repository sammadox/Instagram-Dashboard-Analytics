import csv
from collections import Counter
import pycountry

def get_country_code(country_name):
    try:
        country = pycountry.countries.lookup(country_name)
        return country.alpha_2  # Return the 2-letter country code
    except LookupError:
        return None  # Country name not found

def read_csv_and_create_data_structure(csv_filename):
    csv_file_path = f'{csv_filename}'  # Path to the CSV file

    nationality_counts = Counter()
    total_rows = 0

    # First pass: Count occurrences of each nationality and total rows
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            nationality = row.get('nationality')
            if nationality:
                nationality_counts[nationality] += 1
                total_rows += 1

    # Second pass: Calculate percentage and create the data structure
    data = []
    for nationality, count in nationality_counts.items():
        percentage = (count / total_rows) * 100  # Calculate percentage
        data.append({
            'country': nationality,
            'index': percentage
        })

    # Print the data structure
    print(data)
    return data

# Run the function with the specified CSV file
read_csv_and_create_data_structure('user_data.csv')
