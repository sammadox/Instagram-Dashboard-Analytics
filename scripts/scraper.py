from apify_client import ApifyClient
import json

def fetch_instagram_data(username, api_token, output_file='data.json'):
    # Initialize the ApifyClient with your Apify API token
    client = ApifyClient(api_token)

    # Prepare the Actor input
    run_input = { "usernames": [username] }

    # Run the Actor and wait for it to finish
    run = client.actor("apify/instagram-profile-scraper").call(run_input=run_input)

    # Fetch the results from the Actor's dataset
    dataset = client.dataset(run["defaultDatasetId"])
    items = list(dataset.iterate_items())

    # Save the results to output_file
    with open(output_file, 'w') as f:
        json.dump(items, f, indent=4)

# Example usage
