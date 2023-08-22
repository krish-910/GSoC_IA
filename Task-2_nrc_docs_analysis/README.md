### Entity_Extraction.py

*Description:*
This script performs Named Entity Recognition (NER) using the spaCy library to extract entities of specific types (e.g., organizations, persons) from a given input text. It preprocesses the input data, extracts entities, and counts the frequency of each entity type. The top entities are then stored in a Clustergrammer-compatible format for further analysis.

*Usage:*
1. Make sure you have the spaCy library installed.
2. Specify the input file path containing the text data.
3. Customize the `entity_types_to_keep` list with the desired entity types.
4. Run the script.

*Output:*
The script generates a Clustergrammer-compatible output file containing the document titles and the frequency of each entity in the top entities list.

---

### Task-2.py

*Description:*
This script is part of a larger task and performs multiple operations, including retrieving text file URLs from the Internet Archive, downloading text files, preprocessing text data, performing document clustering using TF-IDF and KMeans, and analyzing clusters. It uses multithreading to enhance efficiency and implements retry mechanisms for URL retrieval.

*Usage:*
1. Make sure you have the required libraries and packages installed (`internetarchive`, `concurrent.futures`, `requests`, `tenacity`, `spacy`, `gzip`, etc.).
2. Customize the `collection_id` variable to the desired Internet Archive collection.
3. Configure logging settings if necessary.
4. Run the script.

*Output:*
The script provides cluster analysis results and execution time information, including the URLs retrieved, downloaded, and processed.

---

### Top_10_Topic_Cluster.py

*Description:*
This script processes preprocessed text data and identifies the top 10 most frequent topics in the documents. It creates a Clustergrammer-compatible matrix indicating the presence of these topics in each document and saves the results in an output file.

*Usage:*
1. Ensure you have the necessary input file (`output.txt`) containing preprocessed text data and document markers.
2. Run the script.

*Output:*
The script generates a Clustergrammer-compatible output file with rows representing documents and columns representing the top 10 topics, along with binary indicators of topic presence.

---

### Top_50_Orgs_Cluster.py

*Description:*
This script processes preprocessed text data and extracts organizations' named entities. It identifies the top 50 most frequently occurring organizations, creates a Clustergrammer-compatible matrix indicating the frequency of these organizations in each document, and saves the results in an output file.

*Usage:*
1. Ensure you have the necessary input file (`output.txt`) containing preprocessed text data and document markers.
2. Run the script.

*Output:*
The script generates a Clustergrammer-compatible output file with rows representing documents and columns representing the top 50 organizations, along with frequency values.

---

### Top_50_Person_Cluster.py

*Description:*
This script processes preprocessed text data and extracts persons' named entities. It identifies the top 50 most frequently occurring persons, creates a Clustergrammer-compatible matrix indicating the frequency of these persons in each document, and saves the results in an output file.

*Usage:*
1. Ensure you have the necessary input file (`output.txt`) containing preprocessed text data and document markers.
2. Run the script.

*Output:*
The script generates a Clustergrammer-compatible output file with rows representing documents and columns representing the top 50 persons, along with frequency values.

---

### Warc_Reader.py

*Description:*
This script processes URLs pointing to WARC (Web ARChive) files, extracts data from PDF files contained in those WARCs using pdfminer, and saves the extracted data along with problematic PDFs to an output file. It iterates through the records in the WARC archive and handles various content types.

*Usage:*
1. Ensure you have the necessary libraries and packages installed (`warcio`, `requests`, `pdfminer`).
2. Specify the input file path containing the URLs (`text_files_urls.txt`).
3. Run the script.

*Output:*
The script generates an output file (`output.txt`) with extracted data, URLs, and information about problematic PDFs.

---
