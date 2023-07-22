import spacy

# Load the spaCy model
nlp = spacy.load('en_core_web_sm')
nlp.max_length = 3000000

# Entity types to keep
entity_types_to_keep = ['PERSON', 'NORP', 'FAC', 'ORG', 'GPE', 'EVENT', 'DATE', 'TOPIC']

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

# Function to extract topics from the text
def extract_topics(text):
    topics = {
        'reactor safety': 'TOPIC',
        'radiation protection': 'TOPIC',
        'regulatory compliance': 'TOPIC',
        'emergency preparedness': 'TOPIC',
        'nuclear security': 'TOPIC',
        'spent fuel management': 'TOPIC',
        'public engagement and outreach': 'TOPIC',
        'nuclear research and development': 'TOPIC',
        'international cooperation': 'TOPIC',
        'regulatory policy and rulemaking': 'TOPIC',
        'nuclear waste disposal': 'TOPIC',
        'nuclear accident investigations': 'TOPIC',
        'nuclear plant inspections': 'TOPIC',
        'nuclear safety culture': 'TOPIC',
        'nuclear emergency exercises': 'TOPIC',
        'nuclear incident reporting': 'TOPIC',
        'nuclear power plant decommissioning': 'TOPIC',
        'nuclear risk assessment': 'TOPIC',
        'nuclear facility security assessments': 'TOPIC',
        'nuclear materials transportation': 'TOPIC',
        'nuclear waste storage': 'TOPIC',
        'radiation monitoring': 'TOPIC',
        'nuclear regulatory framework': 'TOPIC',
        'nuclear licensing process': 'TOPIC',
        'safety analysis and evaluation': 'TOPIC',
        'nuclear emergency response plans': 'TOPIC',
        'nuclear safeguards': 'TOPIC',
        'nuclear energy policy': 'TOPIC',
        'radiation dose limits': 'TOPIC',
        'nuclear fuel cycle': 'TOPIC',
        'nuclear facility design': 'TOPIC',
        'nuclear workforce training': 'TOPIC',
        'nuclear security exercises': 'TOPIC'
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
                    # Remove duplicates from entities
                    for entity_type, entity_list in entities.items():
                        entities[entity_type] = list(set(entity_list))
                    yield {'entities': entities, 'topics': topics}
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
            # Remove duplicates from entities
            for entity_type, entity_list in entities.items():
                entities[entity_type] = list(set(entity_list))
            yield {'entities': entities, 'topics': topics}

# Specify the input file path
input_file = 'output.txt'

# Specify the document marker that signifies the end of each document
document_marker = '<DOCUMENT_END_MARKER>'

# Preprocess the data and extract entities
preprocessed_data = preprocess_data(input_file, document_marker)

# Specify the output file path
output_file = 'entities_output.txt'

# Open the output file in write mode
with open(output_file, 'w', encoding='utf-8') as output_file:
    # Process the preprocessed data
    for doc in preprocessed_data:
        entities = doc['entities']
        entity_text = ", ".join(
            "'{}: [{}]'".format(entity_type, ", ".join(entity_list)) for entity_type, entity_list in entities.items()
        )
        topic_text = ", ".join(
            "'{}: [{}]'".format(topic['entity_type'], topic['text']) for topic in doc['topics']
        )
        output_file.write("\"(%s, %s),\"" % (entity_text, topic_text))

print("Entities output has been written to the file: entities_output.txt")
