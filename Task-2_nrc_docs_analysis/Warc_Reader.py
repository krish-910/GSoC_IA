# Import necessary libraries
import warcio
import requests
from io import BytesIO
import tempfile
from pdfminer.high_level import extract_text
from pdfminer.pdfparser import PDFSyntaxError

# Define a class to process documents
class DocumentProcessor:
    def __init__(self):
        self.urls = []

    def read_urls(self, urls_file_path):
        # Read URLs from the provided file
        with open(urls_file_path, 'r') as urls_file:
            lines = urls_file.readlines()
            for line in lines:
                print(line)
                # Find the index where 'http' starts in the line
                url_start_index = line.find('http')
                if url_start_index != -1:
                    # Extract the URL and add it to the list
                    url = line[url_start_index:].strip()
                    self.urls.append(url)

    def process_documents(self):
        total_pdfs_processed = 0

        for url in self.urls:
            print(f"Processing URL: {url}")
            try:
                # Send an HTTP GET request to the URL
                response = requests.get(url, stream=True)
                print(f"Response status code: {response.status_code}")

                # Create a temporary file to store the response content
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    temp_file.write(response.content)
                    temp_file.seek(0)

                    # Initialize the WARC archive iterator
                    warc_file = warcio.ArchiveIterator(open(temp_file.name, 'rb'))

                    extracted_data = []
                    problematic_files = []

                    # Iterate through the records in the WARC archive
                    for record in warc_file:
                        if record.rec_type == 'response':
                            content_type = record.http_headers.get_header('Content-Type')
                            response_content = record.content_stream().read()

                            if content_type == 'application/pdf':
                                total_pdfs_processed += 1
                                try:
                                    # Extract text from PDF using pdfminer
                                    text = extract_text(BytesIO(response_content))
                                    extracted_data.append(text)
                                    extracted_data.append("<DOCUMENT_END_MARKER>")
                                except PDFSyntaxError as e:
                                    print(f"Error extracting text from PDF: {e}. Skipping this file.")
                                    problematic_files.append(response_content)
                            else:
                                # If not a PDF, add the content as-is
                                extracted_data.append(response_content.decode(errors='ignore'))

                    if extracted_data:
                        # Write extracted data and problematic files to output file
                        with open('output.txt', 'a', encoding='utf-8') as output_file:
                            output_file.write(f"URL: {url}\n")
                            output_file.write(f"Data:\n")
                            output_file.write('\n\n'.join(extracted_data))
                            output_file.write('\n\n')
                            output_file.write(f"Problematic Files:\n")
                            for i, file_content in enumerate(problematic_files):
                                output_file.write(f"Problematic File {i+1}:\n")
                                output_file.write(file_content.decode(errors='ignore'))
                                output_file.write('\n\n')

                        print(f"Added document marker for URL: {url}")
                    else:
                        print(f"No data extracted for URL: {url}")

                    # Close the WARC file
                    warc_file.close()

                    print(f"Finished processing URL: {url}")
            except Exception as err:
                print(f"An error occurred while processing the URL: {url}. Error: {err}")

        print(f"Data extraction and saving completed. Total PDFs processed: {total_pdfs_processed}")

# Entry point of the program
if __name__ == "__main__":
    urls_file_path = 'text_files_urls.txt'  # Path to the file containing URLs
    doc_processor = DocumentProcessor()      # Create an instance of DocumentProcessor class
    doc_processor.read_urls(urls_file_path)  # Read URLs from the file
    doc_processor.process_documents()        # Process the documents and extract data
