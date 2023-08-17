import spacy
import collections
from collections import Counter

# Load the spaCy model
nlp = spacy.load('en_core_web_lg')
nlp.max_length = 3000000

# Entity types to keep
entity_types_to_keep = ['ORG']

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

# Function to preprocess the input data and extract valuable information
def preprocess_data(file_path, document_marker):
    with open(file_path, 'r', encoding='utf-8') as file:
        current_doc = ""
        start_new_doc = False
        for line in file:
            if line.strip() == document_marker:
                start_new_doc = True
                if current_doc:
                    entities = perform_ner(current_doc)
                    yield {'entities': entities}
                    current_doc = ""
            elif start_new_doc:
                current_doc = line.strip() + " "
                start_new_doc = False
            else:
                current_doc += line.strip() + " "
        # Process the last document if it exists
        if current_doc:
            entities = perform_ner(current_doc)
            yield {'entities': entities}

# Specify the input file path
input_file = 'output.txt'

# Specify the document marker that signifies the end of each document
document_marker = '<DOCUMENT_END_MARKER>'

# Preprocess the data and extract entities
preprocessed_data = list(preprocess_data(input_file, document_marker))

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

# Open the output file and write the content
try:
    with open(output_file, 'w', encoding='utf-8') as output_file:
        # Write the header row
        header = "Document\t" + "\t".join(top_50_orgs)
        output_file.write(header + '\n')

        # Write the data rows
        for doc_index, doc in enumerate(preprocessed_data):
            doc_entities = doc['entities']
            data_row = f"Document_{doc_index}\t"
            for org in top_50_orgs:
                frequency = doc_entities.get('ORG', []).count(org)
                data_row += f"{frequency}\t"
            output_file.write(data_row.strip() + '\n')

    print("Data matrix in Clustergrammer format has been written to the file: clustergrammer_input.txt")
except Exception as e:
    print(f"Error occurred while writing the output file: {e}")
