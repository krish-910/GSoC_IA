# GSoC_IA
This repository contains my contributions to the Internet Archive organization as part of the Google Summer of Code (GSoC) program         

--> Task-1.py                                                                                                                                         
This Python File Scan's the given collection of documents and filters the url's for txt files in a compressed txt folder.                                                  
Step-1 -> To run the Task-1.py you need to install internet-archive's python library. Ex - pip install internetarchive.                                                 
Step-2 -> We need to give the collection_id or collection_name of the collection of democracy's library for getting txt urls for the same.                        
Step-3 -> There are two scripts one without progress file which will restart if crashed but is faster and other which tracks the progress with collection_id and count of URL's           which will continue without any argument by taking the collection_id from the progress file. 

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
