# Clustergrammer-Web Integration README

## Introduction
Welcome to the Clustergrammer-Web Integration README. This comprehensive guide outlines the process of using Clustergrammer-Web locally, integrating it with your data extracted from the Nuclear Regulatory Commission (NRC) documents, and also provides details on how to use Clustergrammer via an iframe or its API.

## Why Clustergrammer-Web?
In the realm of data exploration and analysis, Clustergrammer-Web stands as a powerful ally. Its user-friendly interface and dynamic visualization features empower users to make sense of complex data structures quickly. When integrated with data extracted from NRC documents, Clustergrammer-Web transforms raw information into intuitive, interactive visualizations.

## Running Clustergrammer-Web Locally
Before diving into data integration, you need to run Clustergrammer-Web locally. The following steps guide you through the process:

1. *Clone the Clustergrammer Repository:*

   Begin by cloning the Clustergrammer repository from GitHub with this command:

   bash
   git clone -b dev https://github.com/krish-910/clustergrammer-web.git
   

2. *Install Dependencies:*

   Move into the cloned repository's directory and install essential dependencies by executing:

   bash
   pip install -r requirements.txt
   

3. *Start the Clustergrammer Web Application:*

   Launch the Clustergrammer web application by running:

   bash
   python local_run_grammer.py
   

4. *Access the Application:*

   Open your web browser and navigate to http://localhost:9000/clustergrammer to access the Clustergrammer-Web application.

Please ensure that you have Python and pip installed on your system before proceeding with these steps.

## Navigating the Clustergrammer-Web UI

The Clustergrammer-Web application offers a user-friendly interface designed for seamless data exploration and visualization. Here's a brief guide to help you navigate and utilize its features:

1. *Launching the Clustergrammer Web Application:*

   - Refer to the previous section for instructions on starting the Clustergrammer web application.
   - Access the application by opening your web browser and visiting http://localhost:9000/clustergrammer.

2. *Uploading Data:*

   - Locate the "Upload Data" section on the left side of the UI.
   - Use the "Choose File" button to select a data file from your local machine.
   - After selecting the file, click the "Upload" button to load the data into the application.
   - The uploaded data will be displayed in the main area of the UI.

3. *Exploring the Heatmap:*

   - The main UI area showcases the heatmap visualization of your uploaded data.
   - You can zoom in and out of the heatmap using your mouse's scroll wheel or the zoom buttons in the top right corner.
   - Panning the heatmap is as simple as clicking and dragging within the heatmap area.
   - Hovering over a cell in the heatmap reveals additional information about that cell.

4. *Filtering and Sorting:*

   - Utilize the "Filter Rows" and "Filter Columns" input boxes to filter rows and columns based on specific criteria.
   - Enter a keyword or value in the input box and press Enter to apply the filter.
   - To sort rows or columns, click on the respective column or row label in the heatmap.

5. *Saving and Exporting:*

   - For saving the current visualization as an image, use the "Take Snapshot" button located at the top left corner of the UI.
   - To export data in various formats (e.g., png, svg), access the "Export Data" button and select your desired format.

These instructions offer a fundamental understanding of how to use the Clustergrammer-Web application's UI to explore and interact with your data.

## Integration with NRC Data

Now that you are familiar with Clustergrammer-Web's capabilities, you can integrate it with the data extracted from the NRC documents. Prepare your data in TSV format and follow the "Integration Steps" section provided in the earlier README.

## Using Clustergrammer via Iframe or API

### Using Clustergrammer via Iframe

To embed Clustergrammer within an iframe, follow these steps:

# Upload a file to the Clustergrammer web app and visualize using an Iframe
pip install clustergrammer_widget

from clustergrammer import Network

from copy import deepcopy

net = deepcopy(Network())

link = net.Iframe_web_app('clustergrammer_input.txt')

print(link)


### Using Clustergrammer-Web API
To use Clustergrammer-Web's API, follow these steps:
# Using Clustergrammer-Web API

import requests

filename = 'clustergrammer_input.txt'

upload_url = 'http://amp.pharm.mssm.edu/clustergrammer/matrix_upload/'

r = requests.post(upload_url, files={'file': open(filename, 'rb')})

link = r.text

print(link)


These code snippets demonstrate how to upload and visualize data with Clustergrammer via an iframe or its API, extending the flexibility and usability of this powerful tool.

Enjoy harnessing the potent visualization capabilities of Clustergrammer-Web to gain profound insights into your NRC data and easily integrate it into your projects.
