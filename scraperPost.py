from apify_client import ApifyClient
import json

def scrape_posts(username):
    # Initialize the ApifyClient with your Apify API token
    client = ApifyClient("apify_api_fp9UgFVmLHW5kXOM0i0Wlch8atIwFM2g3py6")

    # Prepare the Actor input
    run_input = {
        "username": [username],
        "resultsLimit": 30,
    }

    # Run the Actor and wait for it to finish
    run = client.actor("apify/instagram-post-scraper").call(run_input=run_input)

    # Fetch Actor results from the run's dataset
    dataset = client.dataset(run["defaultDatasetId"])
    items = list(dataset.iterate_items())

    # Save results to data0.5.json
    with open('data0.5.json', 'w') as f:
        json.dump(items, f, indent=4)

    print("Data has been saved to data0.5.json")

