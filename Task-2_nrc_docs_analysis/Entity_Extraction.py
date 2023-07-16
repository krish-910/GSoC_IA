import spacy
import csv

# Load the spaCy model
nlp = spacy.load('en_core_web_sm')
nlp.max_length = 3000000

# Function to perform Named Entity Recognition (NER)
def perform_ner(text):
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        entities.append({
            'text': ent.text,
            'entity_type': ent.label_
        })
    return entities

# Function to extract topics from the text
def extract_topics(text):
    topics = {
        'environmental impact': 'TOPIC',
        'economic assessment': 'TOPIC',
        'safetywalkdown reports': 'TOPIC',
        'radiation protection': 'TOPIC',
        'fire protection': 'TOPIC',
        'radioactive waste': 'TOPIC'
        # Add more topics as needed
    }
    extracted_topics = []
    for topic, entity_type in topics.items():
        if topic in text:
            extracted_topics.append({
                'text': topic,
                'entity_type': entity_type
            })
    return extracted_topics

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
                    topics = extract_topics(current_doc)
                    entity_dict = {}
                    for entity in entities:
                        entity_type = entity['entity_type']
                        if entity_type not in entity_dict:
                            entity_dict[entity_type] = [entity['text']]
                        else:
                            entity_dict[entity_type].append(entity['text'])
                    for topic in topics:
                        entity_type = topic['entity_type']
                        if entity_type not in entity_dict:
                            entity_dict[entity_type] = [topic['text']]
                        else:
                            entity_dict[entity_type].append(topic['text'])
                    yield entity_dict
                    current_doc = ""
            elif start_new_doc:
                current_doc = line.strip() + " "
                start_new_doc = False
            else:
                current_doc += line.strip() + " "
        # Process the last document if it exists
        if current_doc:
            entities = perform_ner(current_doc)
            topics = extract_topics(current_doc)
            entity_dict = {}
            for entity in entities:
                entity_type = entity['entity_type']
                if entity_type not in entity_dict:
                    entity_dict[entity_type] = [entity['text']]
                else:
                    entity_dict[entity_type].append(entity['text'])
            for topic in topics:
                entity_type = topic['entity_type']
                if entity_type not in entity_dict:
                    entity_dict[entity_type] = [topic['text']]
                else:
                    entity_dict[entity_type].append(topic['text'])
            yield entity_dict

# Specify the input file path
input_file = 'output.txt'

# Specify the document marker that signifies the end of each document
document_marker = '<DOCUMENT_END_MARKER>'

# Preprocess the data and extract entities
preprocessed_data = preprocess_data(input_file, document_marker)

# Specify the output file path
output_file = 'entities_output.csv'

# Open the output file in write mode
with open(output_file, 'w', encoding='utf-8', newline='') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(['Entity Type', 'Entities'])

    # Process the preprocessed data
    for entities in preprocessed_data:
        for entity_type, entity_list in entities.items():
            writer.writerow([entity_type, entity_list])

print("Entities output has been written to the file: entities_output.csv")
