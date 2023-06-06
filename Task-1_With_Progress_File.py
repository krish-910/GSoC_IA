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


def save_progress(progress_file_path, collection_id, count):
    with open(progress_file_path, 'w') as f:
        f.write(f"{collection_id}\n{count}")


def load_progress(progress_file_path):
    try:
        with open(progress_file_path) as f:
            content = f.readlines()
            return content[0].strip(), int(content[1])
    except FileNotFoundError:
        return None, 0


def load_collected_urls(file_path):
    try:
        with gzip.open(file_path, 'rt', encoding='utf-8') as file:
            return set(file.read().split('\n\n')[:-1])
    except FileNotFoundError:
        return set()


progress_file = 'progress.txt'
loaded_collection_id, loaded_count = load_progress(progress_file)
if loaded_collection_id and ':' in loaded_collection_id:
    loaded_collection_id = loaded_collection_id.split(':')[1].strip()
    if loaded_collection_id.startswith('{'):
        loaded_collection_id = loaded_collection_id[1:]
    if loaded_collection_id.endswith('}'):
        loaded_collection_id = loaded_collection_id[:-1]

# Create a compressed file to store the redirected text file URLs
file_path = 'text_files_urls.txt.gz'

# Load already collected URLs
collected_urls = load_collected_urls(file_path)

count = loaded_count  # Counter for the number of URLs
lock = threading.Lock()  # Thread lock for synchronized access to count variable

# Initialize requests session
session = requests.Session()


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
def get_item_metadata(item_id):
    return ia.get_item(item_id)


def write_urls(collection_idx_tuple):
    global count
    # Define the media type
    media_type = 'texts'
    collection_idx, collection_id = collection_idx_tuple
    # Get all items in the collection with Media Type - Text
    items = list(ia.search_items('collection:' + collection_id + ' mediatype:' + media_type))
    if loaded_collection_id != '':
        if collection_id == loaded_collection_id:  # Continue only after reaching the last processed collection.
            start_index = max(loaded_count + 1 - count, 0)
    else:
        start_index = 0  # Skip this collection.
        # Set the start index for processing
    items = items[start_index:]

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
                    with lock:
                        current_count = count  # Store current count to ensure accuracy during writing
                        if current_count >= start_index:
                            count += 1
                            if text_file_url not in collected_urls:
                                with gzip.open(file_path, 'at', encoding='utf-8') as file:
                                    file.write(f"{item_name}\n{count}  {text_file_url}\n\n")
                                    # Save progress at every successful URL addition.
                                    save_progress(progress_file, collection_id, count)
                                    collected_urls.add(text_file_url)
        except Exception as e:
            logging.error(f"Error processing item {item_id}: {e}")


# Measure the execution time
start_time = time.time()

# Set the maximum number of concurrent threads
max_threads = 8
# Use multi-threading to process the items concurrently
with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
    futures = []

    skip_until_loaded_item_found = True if loaded_collection_id else False
    for idx, collection_id in enumerate(collection_ids):
        if collection_id == loaded_collection_id:
            print(collection_id)
            print(loaded_collection_id)
            skip_until_loaded_item_found = False
        if not skip_until_loaded_item_found:            
            futures.append(executor.submit(write_urls, (idx, collection_id)))

    # Wait for all tasks to complete
    concurrent.futures.wait(futures)

end_time = time.time()
execution_time = end_time - start_time

print("Total URLs:", count)
print("URLs saved to compressed file:", file_path)
print("Execution time:", execution_time, "seconds")
