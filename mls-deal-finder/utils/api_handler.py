from apify_client import ApifyClient
import logging

def fetch_mls_data(token, actor_id, locations, max_items):
    """
    Initializes the Apify client and triggers the real estate data actor
    to fetch property listings synchronously.
    """
    client = ApifyClient(token)
    all_records = []
    
    for location in locations:
        logging.info(f"Triggering Apify API for location: {location}")
        run_input = {
            "search": location,
            "maxItems": max_items,
            "type": "SALE"
        }
        
        try:
            # Call the actor and wait for it to finish
            run = client.actor(actor_id).call(run_input=run_input)
            
            # Fetch the results from the run's default dataset
            dataset_items = list(client.dataset(run["defaultDatasetId"]).list_items().items)
            logging.info(f"Successfully retrieved {len(dataset_items)} items for {location}")
            all_records.extend(dataset_items)
            
        except Exception as e:
            logging.error(f"API call failed for location {location}: {e}")
            print(f"Error fetching data for {location}. Check logs/api.log for details.")
            
    return all_records
