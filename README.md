# Google Summer of Code 2023 Final Work
This repository contains my contributions to the Internet Archive organization as part of the Google Summer of Code (GSoC) program 

![final](https://github.com/krish-910/GSoC_IA/assets/77330476/9148986c-d16a-4291-ba2c-029d0f85d4c0)

# Introduction
Name: Krish Shewani

Organisation: Internet Archive

Project link: https://summerofcode.withgoogle.com/programs/2023/projects/MMFObnCX 

Project Name: Improving Democracy’s Library

Project Summary: Interactive Analysis of NRC Gov Data

In the quest for advancing regulatory transparency and promoting public engagement, the aim is to transform the vast repository of Nuclear Regulatory Commission (NRC) government data into an interactive and insightful resource. By leveraging a collection of carefully crafted scripts, this initiative seeks to provide users with the ability to explore, analyze, and gain meaningful insights from the NRC's documents and reports.

# About the Organisation
The Internet Archive, a 501(c)(3)non-profit, is building a digital library of Internet sites and other cultural artifacts in digital form. Like a paper library, They provide free access to researchers, historians, scholars, people with print disabilities, and the general public. Their mission is to provide Universal Access to All Knowledge.

Today their archive contains:

735 billion web pages

41 million books and texts

14.7 million audio recordings (including 240,000 live concerts)

8.4 million videos (including 2.4 million Television News programs)

4.4 million images

890,000 software programs

# Contributions during GSoC:
## Summary of Contributions to Internet Archive via GSoC

As a dedicated contributor to the Internet Archive organization through the Google Summer of Code (GSoC) program, I embarked on a transformative project aimed at enhancing the accessibility and comprehensibility of the Nuclear Regulatory Commission (NRC) documents. This ambitious endeavor was driven by the overarching goal of promoting regulatory transparency and empowering the public to actively engage with this valuable repository of information.

## The Challenge: Enhancing Accessibility and Comprehension
The NRC's extensive collection of documents presented a formidable challenge due to its sheer volume and complexity, making it a daunting task for users to navigate and extract meaningful insights. In response to this challenge, my mission was to architect a multifaceted solution that would empower users to not only access these documents but also decipher their significance.

## The Solution: Empowering Users with Interactive Tools

My solution involved the development of a series of meticulously crafted Python scripts, each possessing a unique role and contributing to the overarching mission:

1. *Entity Extraction: Identifying Key Players and Stakeholders*
   - Leveraged the power of Named Entity Recognition (NER) through the spaCy library to pinpoint organizations and individuals mentioned within the text.
   - Aggregated and analyzed entity frequencies, providing users with valuable insights into the key players and stakeholders shaping the regulatory landscape.

2. *Data Extraction and Analysis: Uncovering Patterns and Similarities*
   - Engineered a comprehensive script that seamlessly retrieved text file URLs from the Internet Archive, fetched the corresponding files, and preprocessed the textual data.
   - Applied sophisticated techniques, including TF-IDF and KMeans clustering algorithms, to perform document clustering. This intelligent categorization unveiled hidden patterns and similarities within the vast corpus of documents.

3. *Identifying Top Topics: A Quick Overview of Significant Themes*
   - Pioneered a script designed to identify and rank the top 10 most frequently occurring topics within the preprocessed text data.
   - By visualizing the prevalence of these topics across documents, users were provided with a concise overview of the most pivotal themes encapsulated within the NRC documents.

4. *Organizations and Persons: Understanding Key Entities*
   - Articulated two distinct scripts, each devoted to extracting and ranking the top 50 organizations and individuals most frequently referenced in the documents.
   - Through the dynamic visualization of entity frequencies across documents, users were empowered to recognize the pivotal organizations and influential individuals contributing to the regulatory landscape.

5. *Making PDF Content Accessible: Adding Depth to the Data Pool*
   - Developed a specialized script tailored to process URLs pointing to WARC files containing PDF documents.
   - Employed the pdfminer library to extract data from PDFs, ensuring that all documents, regardless of format, were accessible for exploration and analysis.

## The Vision: Empowering Users to Explore and Engage
These scripts functioned synergistically, creating an enriched environment where users could extract profound insights, grasp the nuances of the regulatory landscape, and engage with the information on a more profound level.

## Visualizing the Data: Clustergrammer-Web Integration
To amplify data accessibility and visualization, I seamlessly integrated the project with Clustergrammer-Web. This transformative integration facilitated the conversion of data from the TSV format into a visually engaging clustering heatmap. Users could now interactively explore the NRC data, gaining deeper comprehension and understanding.

## Conclusion: Advancing Regulatory Transparency and Public Engagement*
Through the culmination of these efforts, I significantly advanced regulatory transparency and heightened public engagement with the NRC documents. The ensemble of developed scripts, coupled with the Clustergrammer-Web integration, made regulatory information not only accessible but also comprehensible. This project represents a pivotal milestone in enhancing the usability and accessibility of government data, ultimately empowering the public to actively participate in the regulatory discourse.


*For a more comprehensive and detailed description, please refer to the readme file located in the respective folder for the task. It contains all the necessary information and instructions to use the scripts successfully.*


# Overall Vision: 

Through the coordinated execution of these scripts, the vision is to create an enriched environment for users to explore NRC government data interactively. The scripts facilitate the extraction of meaningful entities, identification of frequent topics, and analysis of document clusters, organizations, and persons. The resulting Clustergrammer-compatible matrices offer users a dynamic interface to navigate and comprehend the NRC's vast repository, fostering better understanding and engagement with regulatory information.

# Acknowledgements
I am deeply grateful to Google for organizing the Google Summer of Code initiative, which has provided an incredible opportunity for me to contribute to the open-source community. This program has not only facilitated my personal development but has also motivated those around me to engage in open-source projects.

I want to sincerely thank my mentor Vangelis Banos (https://github.com/vbanos) for the invaluable support and guidance they provided throughout the program. Their expertise and insights have played a crucial role in shaping my path and ensuring the success of my project.

Participating in this program has been an enriching and transformative experience, allowing me to delve into the realm of software engineering, enhance my research skills, and contribute meaningfully to the open-source community.
