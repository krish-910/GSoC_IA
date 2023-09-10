import spacy
from collections import Counter
import internetarchive as ia
import logging
import warcio
import requests
from io import BytesIO
import tempfile

# Load the spaCy model
nlp = spacy.load('en_core_web_sm')
nlp.max_length = 3000000

'''
# Collection-Name
collection_id = 'nuclear-regulatory-commission-docs'
'''

# Specify the path to the text file containing URLs
urls_file_path = 'text_files_urls.txt'

# Configure logging
logging.basicConfig(filename='error.log', level=logging.ERROR)

# Entity types to keep
entity_types_to_keep = ['ORG']

def generate_pdf_urls_from_warcs(urls_file_path):	
    # Read the URLs from the provided file	
    urls = []	
    with open(urls_file_path, 'r') as urls_file:	
        lines = urls_file.readlines()	
        for line in lines:	
            # Extract the URL from the line	
            url_start_index = line.find('http')	
            if url_start_index != -1:	
                url = line[url_start_index:].strip()	
                urls.append(url)	
    # Initialize a list for storing PDF URLs	
    pdf_urls = []	
    # Iterate over each URL	
    for url in urls:	
        print(f"Processing URL: {url}")	
        # Download the WARC file as an HTTP stream	
        response = requests.get(url, stream=True)	
        print(f"Response status code: {response.status_code}")	
        # Save the response content to a temporary file	
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:	
            temp_file.write(response.content)	
            temp_file.seek(0)	
            # Open the temporary file as a GZIP-compressed WARC file	
            warc_file = warcio.ArchiveIterator(open(temp_file.name, 'rb'))	
            # Iterate over each record in the WARC file	
            for record in warc_file:	
                # Process response records containing PDF files	
                if record.rec_type == 'response' and record.http_headers.get_header('Content-Type') == 'application/pdf':	
                    # Get the URL of the PDF	
                    pdf_url = record.rec_headers.get_header('WARC-Target-URI')	
                    pdf_urls.append(pdf_url)	
        print(f"Finished processing URL: {url}")	
    return pdf_urls

# Function to perform Named Entity Recognition (NER)
def perform_ner(text):
    doc = nlp(text)
    entities = {entity_type: [] for entity_type in entity_types_to_keep}
    for ent in doc.ents:
        if ent.label_ in entity_types_to_keep:
            entity_type = ent.label_
            entity_text = ent.text
            if entity_text not in entities[entity_type]:
                entities[entity_type].append(entity_text)
    return entities

def get_item_metadata(item_id):	
    return ia.get_item(item_id)	

'''
def extract_Document_Title(collection_id):
    Document_Titles = []

    # Define the media type
    media_type = 'web'

    # Get all items in the collection with Media Type - Text
    items = list(ia.search_items('collection:' + collection_id + ' mediatype:' + media_type))
    for item in items[:2]:
        item_id = item['identifier']
        item_metadata_url = f"https://archive.org/metadata/{item_id}"
        try:
            # Retrieve metadata for the item
            item_metadata = get_item_metadata(item_id)
            item_name = item_metadata.metadata['title']
            # Look for the text file with format warc.gz'
            for file in item_metadata.files:
                if file['name'].endswith('.warc.gz'):
                    Document_Titles.append(file['name'][:-8])
                    text_file_url = f"https://archive.org/download/{item_id}/{file['name']}"
        except Exception as e:
          logging.error(f"Error processing item {item_id}: {e}")
    return Document_Titles
'''

# Modify the function to extract Document Titles along with PDF URLs
def extract_Document_Title(urls_file_path, pdf_urls):
    Document_Titles = []
    countStart = 0
    countEnd = 0
    # Read the URLs from the provided file
    urls = []
    with open(urls_file_path, 'r') as urls_file:
        lines = urls_file.readlines()
        for line in lines:
            # Extract the URL from the line
            url_start_index = line.find('http')
            if url_start_index != -1:
                url = line[url_start_index:].strip()
                pdf_count = extract_num_pdfs_from_url(url)  # Extract the number of PDFs
                countEnd += pdf_count
                # Remove "https://archive.org/download/" from the URL
                url = url.replace("https://archive.org/download/", "")
                # Remove the filename
                filename_index = url.rfind('/')
                url = url[:-8]
                Title = url[filename_index + 1:]
                TimeStamp = Title[4:-6]

                for pdf_url in pdf_urls[countStart:countEnd]:
                    Document_Title = TimeStamp + "/" + pdf_url
                    Document_Titles.append(Document_Title)
                countStart = countEnd

    return Document_Titles

# Function to extract the number of PDFs from a URL
def extract_num_pdfs_from_url(url):
    response = requests.get(url)
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(response.content)
        temp_file.seek(0)

        warc_file = warcio.ArchiveIterator(open(temp_file.name, 'rb'))
        pdf_count = sum(1 for record in warc_file if record.rec_type == 'response' and record.http_headers.get_header('Content-Type') == 'application/pdf')
    return pdf_count


# Function to preprocess the input data and extract valuable information
def preprocess_data(file_path, document_marker, pdf_urls):
    with open(file_path, 'r', encoding='utf-8') as file:
        current_doc = ""
        current_title = ""  # Store the current title
        start_new_doc = False
        for line in file:
            if line.strip() == document_marker:
                start_new_doc = True
                if current_doc:
                    entities = perform_ner(current_doc)
                    yield {'entities': entities, 'title': current_title}
                    current_doc = ""
            elif start_new_doc:
                current_doc = line.strip() + " "
                current_title = line.strip()  # Store the current title
                start_new_doc = False
            else:
                current_doc += line.strip() + " "
        # Process the last document if it exists
        if current_doc:
            entities = perform_ner(current_doc)
            yield {'entities': entities, 'title': current_title}

# Specify the input file path
input_file = 'output.txt'

# Specify the document marker that signifies the end of each document
document_marker = '<DOCUMENT_END_MARKER>'

# Generate PDF URLs from WARC files
pdf_urls = generate_pdf_urls_from_warcs(urls_file_path)

# Preprocess the data and extract orgs
preprocessed_data = list(preprocess_data(input_file, document_marker, pdf_urls))

# Specify the output file path
output_file = 'clustergrammer_input.txt'

# Collect unique entities for each entity type across all documents
unique_entities = {entity_type: set() for entity_type in entity_types_to_keep}

# Initialize a dictionary to store the frequency of each organization across all documents
org_frequency = {}

for doc_index, doc in enumerate(preprocessed_data):
    entities = doc['entities']
    for entity_type, entity_list in entities.items():
        unique_entities[entity_type].update(entity_list)
        if entity_type == 'ORG':
            for org in entity_list:
                if org in org_frequency:
                    org_frequency[org] += 1
                else:
                    org_frequency[org] = 1

# Get the top 50 most frequently occurring organizations
top_50_orgs = sorted(org_frequency.keys(), key=lambda x: org_frequency[x], reverse=True)[:50]

# Extract Document Titles along with PDF URLs
Document_Titles = extract_Document_Title(urls_file_path, pdf_urls)

# Open the output file and write the content
try:
    with open(output_file, 'w', encoding='utf-8') as output_file:
        # Write the header row
        header = "Document\t" + "\t".join(top_50_orgs)
        output_file.write(header + '\n')

        # Write the data rows
        for doc_index, doc in enumerate(preprocessed_data):
          if doc_index < len(Document_Titles):
            doc_title = Document_Titles[doc_index]
            pdf_url = "http://web.archive.org/web/" + Document_Titles[doc_index]
            doc_entities = doc['entities']
            # Check if any of the top 10 topics are present in the document
            if any(org in doc_entities['ORG'] for org in top_50_orgs):
                data_row = f'{pdf_url}\t'
                for org in top_50_orgs:
                    frequency = doc_entities.get('ORG', []).count(org)
                    data_row += f"{frequency}\t"
                output_file.write(data_row.strip() + "\n")
          else:
            print(f"Error: doc_index {doc_index} is out of range for Document_Titles")

    print("Data matrix in Clustergrammer format has been written to the file: clustergrammer_input.txt")
except Exception as e:
    print(f"Error occurred while writing the output file: {e}")
