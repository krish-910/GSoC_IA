import internetarchive as ia
import gzip
import concurrent.futures
import time
import logging
from tenacity import retry, stop_after_attempt, wait_exponential
import threading
import os
import requests
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.cluster import KMeans

# Configure logging
logging.basicConfig(filename='error.log', level=logging.ERROR)

# Define the collection names
collection_id = 'nuclear-regulatory-commission-docs'

# Create a compressed file to store the redirected text file URLs
file_path = 'text_files_urls.txt'

count = 0      # Counter for the number of URLs
lock = threading.Lock()  # Thread lock for synchronized access to count variable

# Initialize requests session
session = requests.Session()

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
def get_item_metadata(item_id):
    return ia.get_item(item_id)

def preprocess_text(text):
    # Add your text preprocessing code here
    preprocessed_text = text.lower()  # Placeholder preprocessing step
    return preprocessed_text

def get_redirected_url(url):
    try:
        response = session.head(url, allow_redirects=True)
        return response.url
    except Exception as e:
        logging.error(f"Error getting redirected URL: {e}")
    return url

def write_urls(collection_id):
    global count
    # Define the media type
    media_type = 'web'

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
                    #redirected_url = get_redirected_url(text_file_url)

                    with lock:
                        count += 1
                        current_count = count  # Store current count to ensure accuracy during writing
                        with open(file_path, 'at', encoding='utf-8') as file:
                            file.write(f"{item_name}\n{current_count}  {text_file_url}\n\n")
        except Exception as e:
            logging.error(f"Error processing item {item_id}: {e}")

def extract_metadata_id(url):
    # Example URL: https://archive.org/download/NRC-20230130192125-crawl339/MANIFEST.txt
    parts = url.split('/')
    if len(parts) > 3:
        return parts[len(parts)-3:]
    return None

def get_download_url(metadata_url):
    metadata_response = session.get(metadata_url)
    metadata_json = metadata_response.json()

    # Check if the 'download' key exists in the metadata JSON
    if 'download' in metadata_json['metadata']:
        download_url = metadata_json['metadata']['download']
    else:
        # Log an error message and return None if the 'download' key is not found
        logging.error(f"Download URL not found in metadata for {metadata_url}")
        return None

    return download_url

def download_text_files(file_urls, download_path):
    os.makedirs(download_path, exist_ok=True)

    for url in file_urls:
        metadata_id = extract_metadata_id(url)
        if metadata_id:
            metadata_url = f"https://archive.org/{metadata_id[0]}/{metadata_id[1]}/{metadata_id[2]}"
            #download_url = get_download_url(metadata_url)
            download_url = metadata_url
            # Check if the download URL is not None before proceeding
            if download_url:
                response = session.get(download_url)
                filename = download_url.split('/')[-2]
                filepath = os.path.join(download_path, filename)

                with open(filepath, 'wb') as file:
                    file.write(response.content)


# Measure the execution time
start_time = time.time()

# Step 1: Retrieve the text file URLs from the Internet Archive
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = []
    futures.append(executor.submit(write_urls, collection_id))
    concurrent.futures.wait(futures)


# Step 2: Load the text file URLs from the text file
text_file_urls = []
with open(file_path, 'r', encoding='utf-8') as file:
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
