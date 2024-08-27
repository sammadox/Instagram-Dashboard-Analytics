import instaloader
import csv
import time
import logging
import requests
import random

# Initialize Instaloader
L = instaloader.Instaloader()

# Fetch proxy list from the API
proxy_url = "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc"
response = requests.get(proxy_url)
proxies = response.json()['data']

# Extract the proxy details and format them
proxy_list = []
for proxy in proxies:
    ip = proxy['ip']
    port = proxy['port']
    protocol = 'http' if 'http' in proxy['protocols'] else 'https'
    proxy_list.append(f"{protocol}://{ip}:{port}")

# Function to set a new proxy for Instaloader
def set_new_proxy(L, proxy_list):
    selected_proxy = random.choice(proxy_list)
    print(f"Using proxy: {selected_proxy}")
    L.context._session.proxies = {"http": selected_proxy, "https": selected_proxy}

# Set up logging
logging.basicConfig(level=logging.INFO)

# Function to try a given operation with retries
def try_with_proxy(L, func, *args, **kwargs):
    retries = len(proxy_list)
    for _ in range(retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error: {e}")
            set_new_proxy(L, proxy_list)
            time.sleep(2)  # Optional delay before retrying
    return None

# Define your functions using the retry mechanism
def check_verified(username):
    return try_with_proxy(L, lambda: instaloader.Profile.from_username(L.context, username).is_verified)

def is_follower_count_in_range(username):
    return try_with_proxy(L, lambda: 500 <= instaloader.Profile.from_username(L.context, username).followers <= 1000)

def is_following_count_in_range(username):
    return try_with_proxy(L, lambda: 500 <= instaloader.Profile.from_username(L.context, username).followees <= 1000)

def check_follower_followee_ratio(username):
    return try_with_proxy(L, lambda: 0.5 <= (instaloader.Profile.from_username(L.context, username).followers /
                                              instaloader.Profile.from_username(L.context, username).followees) <= 2.0)

def calculate_profile_completion(username):
    def completion_func():
        profile = instaloader.Profile.from_username(L.context, username)
        fields = {
            'username': profile.username,
            'full_name': profile.full_name,
            'is_private': profile.is_private,
            'is_verified': profile.is_verified,
            'profile_pic_url': profile.profile_pic_url,
            'bio': profile.biography,
            'followers': profile.followers,
            'followees': profile.followees,
            'posts': profile.mediacount
        }
        completed_fields = sum(bool(value) for value in fields.values())
        completion_percentage = (completed_fields / len(fields)) * 100
        return completion_percentage >= 70
    
    return try_with_proxy(L, completion_func)

# Set an initial proxy
set_new_proxy(L, proxy_list)

# Function to filter usernames
def filter_usernames(input_csv, output_csv, valid_csv, criteria_functions):
    with open(input_csv, mode='r', encoding='utf-8') as infile, \
         open(output_csv, mode='w', newline='', encoding='utf-8') as outfile, \
         open(valid_csv, mode='w', newline='', encoding='utf-8') as validfile:
        
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        valid_writer = csv.writer(validfile)
        
        headers = next(reader, None)
        if headers:
            writer.writerow(headers)
            valid_writer.writerow(headers)
        
        for row in reader:
            username = row[1]
            try:
                results = [criteria_function(username) for criteria_function in criteria_functions]

                logging.info(f"{username}: Criteria function results: {results}")

                if any(results):  # Check if at least one criterion is met
                    logging.info(f"{username} meets one or more criteria.")
                    valid_writer.writerow(row)
                else:
                    logging.info(f"{username} does not meet criteria.")
                    writer.writerow(row)
            except Exception as e:
                logging.error(f"Error processing {username}: {e}")
                writer.writerow(row)
                continue
            time.sleep(2)  # Delay to avoid hitting rate limits

# Usage
filter_usernames('instaExport-2024-08-15T09_17_30.471Z.csv', 
                 'filtered_usernames.csv', 
                 'valid_usernames.csv',
                 [is_follower_count_in_range, 
                  is_following_count_in_range, 
                  check_follower_followee_ratio, 
                  check_verified, 
                  calculate_profile_completion])
