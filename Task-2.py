import os
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

import argparse
import internetarchive as ia
import gzip
import concurrent.futures
import time
import logging
from tenacity import retry, stop_after_attempt, wait_exponential

# Configure logging
logging.basicConfig(filename='error.log', level=logging.ERROR)

# Define the collection names
collection_id = nuclear-regulatory-commission-docs

# Create a compressed file to store the redirected text file URLs
file_path = 'text_files_urls.txt.gz'

count = 0      # Counter for the number of URLs
lock = threading.Lock()  # Thread lock for synchronized access to count variable

# Initialize requests session
session = requests.Session()

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
def get_item_metadata(item_id):
    return ia.get_item(item_id)

def write_urls(collection_id):
    global count
    # Define the media type
    media_type = 'text'

    # Get all items in the collection with Media Type - Text
    items = list(ia.search_items('collection:' + collection_id + ' mediatype:' + media_type))

    for item in items:
        item_id = item['identifier']
        item_metadata_url = f"https://archive.org/metadata/{item_id}"
        try:
            # Retrieve metadata for the item
            item_metadata = get_item_metadata(item_id)
            item_name = item_metadata.metadata['title']

            # Look for the text file with format 'DjVuTXT' and name like '*.txt'
            for file in item_metadata.files:
                if file['name'].endswith('.txt'):
                    text_file_url = f"https://archive.org/download/{item_id}/{file['name']}"
                    # redirected_url = get_redirected_url(text_file_url)

                    with lock:
                        count += 1
                        current_count = count  # Store current count to ensure accuracy during writing
                        with gzip.open(file_path, 'at', encoding='utf-8') as file:
                            file.write(f"{item_name}\n{current_count}  {text_file_url}\n\n")
        except Exception as e:
            logging.error(f"Error processing item {item_id}: {e}")

def download_text_files(file_urls, download_path):
    os.makedirs(download_path, exist_ok=True)

    for url in file_urls:
        response = session.get(url)
        filename = url.split('/')[-1]
        filepath = os.path.join(download_path, filename)

        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(response.text)

def preprocess_text(text):
    # Add your text preprocessing code here
    preprocessed_text = text.lower()  # Placeholder preprocessing step
    return preprocessed_text

# Measure the execution time
start_time = time.time()

# Step 1: Retrieve the text file URLs from the Internet Archive
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = []
    for collection_id in collection_ids:
        futures.append(executor.submit(write_urls, collection_id))
    concurrent.futures.wait(futures)

# Step 2: Load the redirected text file URLs from the compressed file
text_file_urls = []
with gzip.open(file_path, 'rt', encoding='utf-8') as file:
    for line in file:
        if line.strip():
            _, url = line.strip().split(' ', 1)
            text_file_urls.append(url)

# Step 3: Download the text files
download_path = 'text_files'
download_text_files(text_file_urls, download_path)

# Step 4: Preprocess the text data
preprocessed_texts = []
for url in text_file_urls:
    filename = url.split('/')[-1]
    filepath = os.path.join(download_path, filename)

    with open(filepath, 'r', encoding='utf-8') as file:
        text = file.read()
        preprocessed_text = preprocess_text(text)
        preprocessed_texts.append(preprocessed_text)

# Step 5: Vectorize the text data
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(preprocessed_texts)

# Step 6: Perform document clustering
num_clusters = 5
kmeans = KMeans(n_clusters=num_clusters)
kmeans.fit(X)

# Step 7: Analyze and interpret the clusters
cluster_labels = kmeans.labels_
for i in range(num_clusters):
    cluster_docs = [text_file_urls[j] for j, label in enumerate(cluster_labels) if label == i]
    print(f"Cluster {i+1}:")
    for doc in cluster_docs:
        print(doc)
    print()

end_time = time.time()
execution_time = end_time - start_time

print("Total URLs:", count)
print("URLs saved to compressed file:", file_path)
print("Execution time:", execution_time, "seconds")
