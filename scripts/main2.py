import json
import csv
from langdetect import detect
import pycountry
from .Modules.FollowersLanguage import get_language_from_country_code
from .Modules.AgeDetection import GetAgeandGender
import random
import pandas as pd


def random_gender():
    return random.choice(["Man", "Woman"])

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
    ff_list=[]

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
            lang=get_language_from_country_code(country_code)
            try:
                age_gender=GetAgeandGender(profile_pic_url)
                age=age_gender[0]
                gender=age_gender[1]
            except:
                age=30
                gender=random_gender()
                ff_list.append(comment.get("ownerUsername"))
                print(ff_list)# Generate one random selection
            if username:
                # Store data in the dictionary, avoiding repetition
                if username not in user_data:
                    user_data[username] = {
                        'text': text,
                        'profile_pic_url': profile_pic_url,
                        'nationality':nat,
                        'country_code':country_code,
                        'language':lang,
                        'age':age,
                        'gender':gender
                    }

    # Write the user data to a CSV file
    with open(output_csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # Write the header
        writer.writerow(['username', 'text', 'profile_pic_url','nationality','country_code','language','age','gender'])

        # Write the data for each user
        for username, data in user_data.items():
            writer.writerow([username, data['text'], data['profile_pic_url'],data['nationality'],data['country_code'],data['language'],data['age'],data['gender']])

    # Print the number of unique usernames extracted
    print(f"Extracted {len(user_data)} unique users to {output_csv_file}")
    print(len(ff_list))
    print(len(user_data))
def process_csv_file(filename):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(filename)

    # Replace the 'Man' values with 'Male' and map the gender values correctly
    df['gender'] = df['gender'].replace({'Man': 'Male', 'Woman': 'Female'})

    # Create an age group column based on the 'age' values
    def categorize_age(age):
        if 20 <= age <= 29:
            return '20-29'
        elif 30 <= age <= 39:
            return '30-39'
        elif 40 <= age <= 49:
            return '40-49'
        else:
            return 'Other'

    df['age_group'] = df['age'].apply(categorize_age)

    # Count the occurrences of each age group and gender combination
    grouped_data = df.groupby(['age_group', 'gender']).size().reset_index(name='Count')

    # Create the final data structure
    age_groups = ['20-29', '30-39', '40-49']
    genders = ['Male', 'Female']

    # Initialize the data structure with default values
    data = {
        'Age Group': [],
        'Gender': [],
        'Count': []
    }

    # Fill the data structure
    for age_group in age_groups:
        for gender in genders:
            count = grouped_data[(grouped_data['age_group'] == age_group) & (grouped_data['gender'] == gender)]['Count']
            if not count.empty:
                data['Age Group'].append(age_group)
                data['Gender'].append(gender)
                data['Count'].append(count.values[0])
            else:
                data['Age Group'].append(age_group)
                data['Gender'].append(gender)
                data['Count'].append(0)

    return data
# Run the function with the specified JSON files
#data=process_csv_file('user_data.csv')
#print(data)