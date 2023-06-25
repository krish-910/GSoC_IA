import warcio
import requests
from io import BytesIO
import tempfile
from pdfminer.high_level import extract_text
from pdfminer.pdfparser import PDFSyntaxError

# Read the URLs from text_files_urls.txt
urls = []
with open('text_files_urls.txt', 'r') as urls_file:
    lines = urls_file.readlines()
    for line in lines:
        # Extract the URL from the line
        url_start_index = line.find('http')
        if url_start_index != -1:
            url = line[url_start_index:].strip()
            urls.append(url)

print(f"Total URLs: {len(urls)}")

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

        # Initialize a list for storing extracted PDF text
        extracted_text = []

        # Initialize a list for storing problematic PDF files
        problematic_files = []

        # Iterate over each record in the WARC file
        for record in warc_file:
            # Process response records containing PDF files
            if record.rec_type == 'response' and record.http_headers.get_header('Content-Type') == 'application/pdf':
                # Extract the response content (PDF)
                response_content = record.content_stream().read()

                # Extract text from the PDF file
                with BytesIO(response_content) as pdf_buffer:
                    try:
                        text = extract_text(pdf_buffer)
                        extracted_text.append(text)
                    except PDFSyntaxError as e:
                        print(f"Error extracting text from PDF: {e}. Skipping this file.")
                        problematic_files.append(response_content)

        # Save the extracted text in output.txt
        with open('output.txt', 'a', encoding='utf-8') as output_file:
            output_file.write(f"URL: {url}\n")
            output_file.write(f"Text:\n")
            output_file.write('\n\n'.join(extracted_text))
            output_file.write('\n\n')

        # Save the problematic PDF files
        for i, file_content in enumerate(problematic_files):
            with open(f'problematic_pdf_{i+1}.pdf', 'wb') as pdf_file:
                pdf_file.write(file_content)

    # Close the WARC file
    warc_file.close()

    print(f"Finished processing URL: {url}")

print("Data extraction and saving completed.")
