import warcio
import requests
from bs4 import BeautifulSoup
import gzip
from sanitize_filename import sanitize
from PyPDF2 import PdfReader
from io import BytesIO

# Open the GZIP-compressed WARC file
warc_file = 'NRC-20230130192125-00001.warc.gz'
with gzip.open(warc_file, 'rb') as gzipped_warc:
    # Create an ArchiveIterator for the GZIP-compressed WARC file
    warc_iterator = warcio.archiveiterator.ArchiveIterator(gzipped_warc)

    # Initialize variables for storing URLs and links
    urls = []
    links = []

    # Iterate over each record in the WARC file
    for record in warc_iterator:
        # Process response records containing PDF files
        if record.rec_type == 'response' and record.http_headers.get_header('Content-Type') == 'application/pdf':
            # Extract the URL and response content
            url = record.rec_headers.get_header('WARC-Target-URI')
            response_content = record.content_stream().read()

            # Extract text from the PDF file
            with BytesIO(response_content) as pdf_buffer:
                pdf = PdfReader(pdf_buffer)
                text = ' '.join([page.extract_text() for page in pdf.pages])

                # Save the extracted text in output.txt
                with open('output.txt', 'a', encoding='utf-8') as output_file:
                    output_file.write(f"URL: {url}\n")
                    output_file.write(f"Text:\n{text}\n\n")

        # Process HTML response records
        elif record.rec_type == 'response' and record.http_headers.get_header('Content-Type') == 'text/html':
            # Extract the URL and response content
            url = record.rec_headers.get_header('WARC-Target-URI')
            response_content = record.content_stream().read()

            # Parse the HTML content
            soup = BeautifulSoup(response_content, 'html.parser')

            # Extract useful data from the HTML, e.g., scrape specific elements
            # Example: Extract all links from the HTML
            extracted_links = [link['href'] for link in soup.find_all('a') if link.get('href')]

            # Add the URL and links to the respective lists
            urls.append(url)
            links.extend(extracted_links)

    # Save the URLs and links in output.txt
    with open('output.txt', 'a', encoding='utf-8') as output_file:
        output_file.write("URLs:\n")
        output_file.write('\n'.join(urls))
        output_file.write("\n\nLinks:\n")
        output_file.write('\n'.join(links))

print("Data extraction and saving completed.")
