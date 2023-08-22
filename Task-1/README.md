# GSoC_IA
This repository contains my contributions to the Internet Archive organization as part of the Google Summer of Code (GSoC) program         

--> Task-1.py                                                                                                                                         

Below is the combined README file for both `task1_with_progress_file.py` and `task1_without_progress_file.py` scripts. The README includes an explanation of both scripts, their usage, and other relevant information:

# Internet Archive Text Files Downloader

The Internet Archive Text Files Downloader is a Python script that allows you to download text files from various collections available on the Internet Archive. The script uses the Internet Archive Python library (`internetarchive`) and `requests` for handling HTTP requests. It supports concurrent downloading using multi-threading to expedite the process.

## Requirements

- Python 3.x
- internetarchive library
- requests library
- tenacity library

## Installation

1. Clone or download this repository to your local machine.

2. Install the required libraries by running the following command:

bash
pip install internetarchive requests tenacity


## Task 1 - Download Text Files with Progress File (`task1_with_progress_file.py`)

### Usage

1. Before running the script, ensure you have the necessary permissions to access the Internet Archive collections.

2. Open the `task1_with_progress_file.py` file in a text editor.

3. Configure the script by modifying the following variables:

   - `collection_info`: A list of dictionaries containing collection names and optional subject filters. Customize this list to specify the collections you want to download text files from.
   - `progress_file`: The name of the file to store the progress of the download process. This file will be used to resume downloads from where they left off.
   - `file_path`: The name of the compressed file to store the redirected text file URLs.

4. Save your changes and close the file.

5. Run the script:

bash
python task1_with_progress_file.py


6. The script will start processing the collections one by one, downloading text files that match the specified criteria. It will utilize multi-threading for concurrent downloads to speed up the process.

7. If the script is interrupted or stopped, it will save the progress in the `progress_file`, allowing you to resume the download later.

### Output

The script will create a compressed file (`text_files_urls.txt.gz`) that contains the URLs of the downloaded text files from the Internet Archive. Each entry in the file includes the item name and the corresponding URL.

### Note

- The script uses the Internet Archive Python library (`internetarchive`) to interact with the Internet Archive API. Make sure you have installed this library before running the script.

- The `requests` library is used to handle HTTP requests for metadata retrieval.

- The `tenacity` library is utilized for retrying requests in case of temporary network or server issues.

- The script processes multiple collections concurrently, using multi-threading to improve performance. You can adjust the `max_threads` variable in the script to control the number of concurrent threads.

- The script will skip already downloaded URLs by checking the `progress_file`. If you want to restart the download for any reason, delete the `progress_file` before running the script.

- Ensure you have proper access rights and permissions to download from the specified collections on the Internet Archive.

- The script is provided as a starting point and can be customized to fit your specific requirements or collections.

## Task 2 - Download Text Files Without Progress File (`task1_without_progress_file.py`)

### Usage

1. Before running the script, ensure you have the necessary permissions to access the Internet Archive collections.

2. Open the `task1_without_progress_file.py` file in a text editor.

3. Configure the script by modifying the following variables:

   - `collection_info`: A list of dictionaries containing collection names and optional subject filters. Customize this list to specify the collections you want to download text files from.
   - `file_path`: The name of the compressed file to store the redirected text file URLs.

4. Save your changes and close the file.

5. Run the script:

bash
python task1_without_progress_file.py


6. The script will start processing the collections one by one, downloading text files that match the specified criteria. It will utilize multi-threading for concurrent downloads to speed up the process.

### Output

The script will create a compressed file (`text_files_urls.txt.gz`) that contains the URLs of the downloaded text files from the Internet Archive. Each entry in the file includes the item name and the corresponding URL.

### Note

- The script uses the Internet Archive Python library (`internetarchive`) to interact with the Internet Archive API. Make sure you have installed this library before running the script.

- The `requests` library is used to handle HTTP requests for metadata retrieval.

- The `tenacity` library is utilized for retrying requests in case of temporary network or server issues.

- The script processes multiple collections concurrently, using multi-threading to improve performance. You can adjust the `max_threads` variable in the script to control the number of concurrent threads.

- Ensure you have proper access rights and permissions to download from the specified collections on the Internet Archive.

- The script is provided as a starting point and can be customized to fit your specific requirements or collections.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
--> Task-2.py

**Entity_Extraction.py
# Named Entity Recognition (NER) and Topic Extraction Script

This script performs Named Entity Recognition (NER) and topic extraction from a text file containing documents. It uses the spaCy library to recognize entities of interest such as persons, organizations, dates, and locations, and extracts predefined topics related to nuclear safety and regulatory aspects. The output is written to a new file, `entities_output.txt`.

## Requirements

- Python 3.x
- spaCy library (make sure to install the required spaCy model before running the script)

## Installation

1. Clone or download this repository to your local machine.

2. Install the required libraries by running the following command:

bash
pip install spacy


3. Download the spaCy English language model by running:

bash
python -m spacy download en_core_web_sm


## Usage

1. Prepare your input text file (`output.txt`) containing one or more documents with a specified document marker (`<DOCUMENT_END_MARKER>`). Each document should be separated by the document marker.

2. Open the `main.py` file and modify the `input_file` and `document_marker` variables to match your input file and document marker, respectively.

3. Customize the `entity_types_to_keep` and `topics` dictionaries in the `perform_ner` and `extract_topics` functions, respectively, to adjust the types of entities you want to keep and the topics you want to extract.

4. Run the script:

bash
python main.py


5. The script will process the input file, perform NER, and extract topics from each document. The results will be written to `entities_output.txt`.

## Customization

### Entity Types to Keep

The `entity_types_to_keep` list determines which entity types will be considered during NER. Modify this list to include or exclude specific types according to your requirements.

### Topics

The `extract_topics` function extracts predefined topics related to nuclear safety and regulatory aspects. You can add, remove, or modify topics in the `topics` dictionary to fit your specific domain or interest.

## Output Format

The output file (`entities_output.txt`) will contain comma-separated entries, where each entry consists of:


"(entities: [entity_type: [entity1, entity2, ...]], topics: [entity_type: [topic1, topic2, ...]]),"


- `entities`: Contains the recognized entities from the input document, grouped by their entity types.
- `topics`: Contains the extracted topics related to nuclear safety and regulatory aspects.

## Note

- The script uses the `en_core_web_sm` spaCy model by default. If you wish to use a different model, modify the `nlp` initialization in the script.

- The `nlp.max_length` is set to handle documents up to 3,000,000 characters long. Adjust this value if your documents are significantly larger or smaller.

- This script is provided as a starting point and may require further customization based on your specific use case.

- For more information on spaCy and NER, please refer to the spaCy documentation: https://spacy.io/usage/linguistic-features#named-entities 