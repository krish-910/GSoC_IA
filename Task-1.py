import internetarchive as ia
import gzip
import concurrent.futures
import time
import logging

# Configure logging
logging.basicConfig(filename='error.log', level=logging.ERROR)

# Define the collection ID
collection_id = 'usdanationalagriculturallibrary'

# Define the media type
media_type = 'texts'

# Retrieve all items in the collection with Media Type - Text
items = list(ia.search_items('collection:' + collection_id + ' mediatype:' + media_type))

# Create a compressed file to store the URLs
file_path = 'text_document_urls.txt.gz'

count = 0  # Counter for the number of URLs

def process_items(chunk):
    global count
    for item in chunk:
        item_id = item['identifier']
        item_url = f"https://archive.org/details/{item_id}"
        try:
            with gzip.open(file_path, 'at', encoding='utf-8') as file:
                count += 1
                file.write(f"{count} {item_url}\n")
        except Exception as e:
            logging.error(f"Error writing URL for item {item_id}: {e}")

# Measure the execution time
start_time = time.time()

# Set the number of threads
num_threads = 6

# Split the items into chunks
chunk_size = (len(items)) // num_threads
item_chunks = [items[i:i+chunk_size] for i in range(0, len(items), chunk_size)]

# Use multi-threading to process the item chunks
with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
    executor.map(process_items, item_chunks)

end_time = time.time()
execution_time = end_time - start_time

print("Total URLs:", count)
print("URLs saved to compressed file:", file_path)
print("Execution time:", execution_time, "seconds")

