import internetarchive as ia
import gzip
import concurrent.futures
import time
import logging
import requests
from tenacity import retry, stop_after_attempt, wait_exponential

# Configure logging
logging.basicConfig(filename='error.log', level=logging.ERROR)

# Define the collection ID
collection_id = 'copyrightrecords'

# Define the media type
media_type = 'texts'

# Get all items in the collection with Media Type - Text
items = list(ia.search_items('collection:' + collection_id + ' mediatype:' + media_type))

# Create a compressed file to store the redirected text file URLs
file_path = 'text_files_urls.txt.gz'

count = 0  # Counter for the number of URLs

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
def get_item_metadata(item_id):
    return ia.get_item(item_id)

def get_redirected_url(url):
    try:
        session = requests.Session()
        response = session.get(url, allow_redirects=True)
        return response.url
    except Exception as e:
        logging.error(f"Error getting redirected URL: {e}")
    return url

def write_urls(item):
    global count
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
                redirected_url = get_redirected_url(text_file_url)

                print(f"Item: {item_name}")
                print(f"Original URL: {text_file_url}")
                print(f"Redirected URL: {redirected_url}")
                print()

                with gzip.open(file_path, 'at', encoding='utf-8') as file:
                    count += 1
                    file.write(f"{item_name} - {count} {redirected_url}\n")
    except Exception as e:
        logging.error(f"Error processing item {item_id}: {e}")

# Measure the execution time
start_time = time.time()

# Set the maximum number of concurrent threads
max_threads = 10

# Use multi-threading to process the items concurrently
with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
    futures = []
    for item in items:
        futures.append(executor.submit(write_urls, item))

    # Wait for all tasks to complete
    concurrent.futures.wait(futures)

end_time = time.time()
execution_time = end_time - start_time

print("Total URLs:", count)
print("URLs saved to compressed file:", file_path)
print("Execution time:", execution_time, "seconds")
