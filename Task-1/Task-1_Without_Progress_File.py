import argparse
import internetarchive as ia
import gzip
import concurrent.futures
import time
import logging
import requests
from tenacity import retry, stop_after_attempt, wait_exponential
import threading

# Configure logging
logging.basicConfig(filename='error.log', level=logging.ERROR)

# Define the collection names and subject filter
collection_info = [
    {'name': 'governmentpublications', 'subject_filter': None},
    {'name': 'USGovernmentDocuments', 'subject_filter': None},
    {'name': 'library_and_archives_canada', 'subject_filter': None},
    {'name': 'fedlink', 'subject_filter': None},
    {'name': 'ualbertaeducationguides', 'subject_filter': None},
    {'name': 'albertagovernmentpublications', 'subject_filter': None},
    {'name': 'lacbac', 'subject_filter': None},
    {'name': 'nasa', 'subject_filter': None},
    {'name': 'us_census', 'subject_filter': None},
    {'name': 'sim_microfilm', 'subject_filter': 'Government Documents'}
]
collection_ids = []
collection_count = 0
# Iterate over the collection names and subject filters
for collection_info in collection_info:
    collection_name = collection_info['name']
    subject_filter = collection_info['subject_filter']

    # Define the collection ID
    collection_id = collection_name

    # Define the media type
    media_type = 'collection'

    # Construct the query based on the collection and subject filter
    query = f'collection:{collection_id} mediatype:{media_type}'
    if subject_filter:
        query += f' AND subject:"{subject_filter}"'

    collection_items = list(ia.search_items(query))

    # Print the name and count of items in the collection
    print(f"Collection: {collection_name}, Count: {len(collection_items)}")
    for item in collection_items:
        item_metadata = ia.get_item(item['identifier'])
        item_title = item_metadata.metadata['identifier']
        collection_count = collection_count + 1
        collection_ids.append(item_title)
    print()
print(collection_count)

# Create a compressed file to store the redirected text file URLs
file_path = 'text_files_urls.txt.gz'



count = 0      # Counter for the number of URLs
lock = threading.Lock()  # Thread lock for synchronized access to count variable

# Initialize requests session
session = requests.Session()

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
def get_item_metadata(item_id):
    return ia.get_item(item_id)
'''
def get_redirected_url(url):
    try:
        response = session.head(url, allow_redirects=True)
        return response.url
    except Exception as e:
        logging.error(f"Error getting redirected URL: {e}")
    return url
'''

def write_urls(item):
    global count
    # Define the media type
    media_type = 'texts'

    # Get all items in the collection with Media Type - Text
    items = list(ia.search_items('collection:' + item + ' mediatype:' + media_type))

    for item in items:
      item_id = item['identifier']
      item_metadata_url = f"https://archive.org/metadata/{item_id}"
      try:
          # Retrieve metadata for the item
          item_metadata = get_item_metadata(item_id)
          item_name = item_metadata.metadata['title']

          # Look for the text file with format 'DjVuTXT' and name like '*.txt'
          for file in item_metadata.files:
              if file['format'] == 'DjVuTXT' and file['name'].endswith('.txt'):
                  text_file_url = f"https://archive.org/download/{item_id}/{file['name']}"
                  #redirected_url = get_redirected_url(text_file_url)

                  with lock:
                      count += 1
                      current_count = count  # Store current count to ensure accuracy during writing
                      with gzip.open(file_path, 'at', encoding='utf-8') as file:
                          file.write(f"{item_name}\n{current_count}  {text_file_url}\n\n")
      except Exception as e:
          logging.error(f"Error processing item {item_id}: {e}")

# Measure the execution time
start_time = time.time()

# Set the maximum number of concurrent threads
max_threads = 8

# Use multi-threading to process the items concurrently
with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
    futures = []
    for collection_id in collection_ids:
        futures.append(executor.submit(write_urls, collection_id))

    # Wait for all tasks to complete
    concurrent.futures.wait(futures)

end_time = time.time()
execution_time = end_time - start_time 

print("Total URLs:", count)
print("URLs saved to compressed file:", file_path)
print("Execution time:", execution_time, "seconds")
