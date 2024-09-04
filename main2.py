import json
import csv
from langdetect import detect
import pycountry

def get_country_code(country_name):
    try:
        country = pycountry.countries.lookup(country_name)
        return country.alpha_2  # Return the 2-letter country code
    except LookupError:
        return None  # Country name not found
    

def TextToNat(text):
    try:
        # Detect the language of the text
        language = detect(text)

        # Map language codes to nationalities
        language_to_nationality = {
    'ko': 'South Korea',
    'en': 'United States',  # This can also be United Kingdom, Canada, Australia, etc.
    'es': 'Spain',  # This can also be Mexico, Argentina, etc.
    'fr': 'France',  # This can also be Belgium, Canada, Switzerland, etc.
    'de': 'Germany',  # This can also be Austria, Switzerland, etc.
    'zh-cn': 'China',
    'ja': 'Japan',
    'ru': 'Russia',
    'it': 'Italy',
    'pt': 'Portugal',  # This can also be Brazil, etc.
    'ar': 'Saudi Arabia',  # This can also be Egypt, Morocco, etc.
    'hi': 'India',
    'bn': 'Bangladesh',
    'pa': 'Pakistan',
    'fa': 'Iran',
    'tr': 'Turkey',
    'nl': 'Netherlands',
    'pl': 'Poland',
    'ro': 'Romania',
    'el': 'Greece',
    'sv': 'Sweden',
    'no': 'Norway',
    'da': 'Denmark',
    'fi': 'Finland',
    'hu': 'Hungary',
    'cs': 'Czech Republic',
    'sk': 'Slovakia',
    'uk': 'Ukraine',
    'bg': 'Bulgaria',
    'sr': 'Serbia',
    'hr': 'Croatia',
    'he': 'Israel',
    'th': 'Thailand',
    'vi': 'Vietnam',
    'ms': 'Malaysia',
    'id': 'Indonesia',
    'tl': 'Philippines',
    'ca': 'Catalonia',  # This is a region in Spain
    'eu': 'Basque Country',  # This is a region in Spain
    'gl': 'Galicia',  # This is a region in Spain
    'lt': 'Lithuania',
    'lv': 'Latvia',
    'et': 'Estonia',
    'mt': 'Malta',
    'hy': 'Armenia',
    'ka': 'Georgia',
    'mn': 'Mongolia',
    'kw': 'Kuwait',
    'lb': 'Lebanon',
    'sy': 'Syria',
    'jo': 'Jordan',
    'iq': 'Iraq',
    'om': 'Oman',
    'qa': 'Qatar',
    'bh': 'Bahrain',
    'ye': 'Yemen',
    'sd': 'Sudan',
    'so': 'Somalia',
    'tz': 'Tanzania',
    'ug': 'Uganda',
    'rw': 'Rwanda',
    'ke': 'Kenya',
    'zm': 'Zambia',
    'zw': 'Zimbabwe',
    'na': 'Namibia',
    'bw': 'Botswana',
    'ls': 'Lesotho',
    'mw': 'Malawi',
    'cv': 'Cape Verde',
    'gq': 'Equatorial Guinea',
    'dj': 'Djibouti',
    'ne': 'Niger',
    'ml': 'Mali',
    'bf': 'Burkina Faso',
    'sn': 'Senegal',
    'gn': 'Guinea',
    'sl': 'Sierra Leone',
    'lr': 'Liberia',
    'tg': 'Togo',
    'ben': 'Benin',
    'ng': 'Nigeria',
    'gh': 'Ghana',
    'et': 'Ethiopia',
    'ae': 'United Arab Emirates',
    'sa': 'Saudi Arabia',
    'bh': 'Bahrain',
    'kw': 'Kuwait',
    'om': 'Oman',
    'qa': 'Qatar',
    'ye': 'Yemen'
}

        # Get the nationality based on the detected language
        nationality = language_to_nationality.get(language, 'Unknown')
    except:
        nationality=""
    return(nationality)

def extract_user_data(json_filename):
    json_file_path = f'{json_filename}'  # Path to the JSON file
    output_csv_file = 'user_data.csv'  # Output CSV file in the same directory

    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)  # Read JSON data from file

    # Use a dictionary to store user data
    user_data = {}

    # Loop through each post and its comments to extract user data
    for post in data:
        for comment in post.get("latestComments", []):  # Get the latestComments for each post
            username = comment.get("ownerUsername")  # Get the ownerUsername from the comment
            profile_pic_url = comment.get("ownerProfilePicUrl")
            text = comment.get("text")
            nat=TextToNat(text)
            country_code=get_country_code(nat)
            if username:
                # Store data in the dictionary, avoiding repetition
                if username not in user_data:
                    user_data[username] = {
                        'text': text,
                        'profile_pic_url': profile_pic_url,
                        'nationality':nat,
                        'country_code':country_code
                    }

    # Write the user data to a CSV file
    with open(output_csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # Write the header
        writer.writerow(['username', 'text', 'profile_pic_url','nationality','country_code'])

        # Write the data for each user
        for username, data in user_data.items():
            writer.writerow([username, data['text'], data['profile_pic_url'],data['nationality'],data['country_code']])

    # Print the number of unique usernames extracted
    print(f"Extracted {len(user_data)} unique users to {output_csv_file}")

# Run the function with the specified JSON file
extract_user_data('data0.5.json')
