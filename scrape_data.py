import requests
from bs4 import BeautifulSoup
import json
import os

# URLs to scrape
urls = [
    
    "https://sites.duke.edu/aipi/new-student-resources/",
    "https://sites.duke.edu/aipi/student-activities/",
    "https://sites.duke.edu/aipi/academic-resources/",
    "https://sites.duke.edu/aipi/career-resources/",
    "https://sites.duke.edu/aipi/industry-resources/",
    "https://sites.duke.edu/aipi/calendar/",
    "https://sites.duke.edu/aipi/2021/04/30/duke-engineering-launches-institute-for-enterprise-engineering/",
    "https://sites.duke.edu/aipi/2021/04/28/hello-world/",

    "https://ai.meng.duke.edu/",
    "https://ai.meng.duke.edu/apply",
    "https://ai.meng.duke.edu/certificate",
    "https://ai.meng.duke.edu/contact",
    "https://ai.meng.duke.edu/courses",
    "https://ai.meng.duke.edu/degree",
    "https://ai.meng.duke.edu/faculty",
    "https://ai.meng.duke.edu/faculty/alfredo-deza",
    "https://ai.meng.duke.edu/faculty/brad-fox",
    "https://ai.meng.duke.edu/faculty/brinnae-bent",
    "https://ai.meng.duke.edu/faculty/jeffrey-glass",
    "https://ai.meng.duke.edu/faculty/jeffrey-ward",
    "https://ai.meng.duke.edu/faculty/jon-reifschneider",
    "https://ai.meng.duke.edu/faculty/lawrence-carin",
    "https://ai.meng.duke.edu/faculty/natalia-summerville",
    "https://ai.meng.duke.edu/faculty/noah-gift",
    "https://ai.meng.duke.edu/faculty/pramod-singh",
    "https://ai.meng.duke.edu/faculty/richard-telford",
    "https://ai.meng.duke.edu/faculty/theodore-ryan",
    "https://ai.meng.duke.edu/faculty/wann-jiun-ma",
    "https://ai.meng.duke.edu/faculty/xu-chen",
    "https://ai.meng.duke.edu/faculty/yiran-chen",
    "https://ai.meng.duke.edu/industry",
    "https://ai.meng.duke.edu/leadership",
    "https://ai.meng.duke.edu/news",
    "https://ai.meng.duke.edu/news/dr-brinnae-bent-joins-duke-ai-master-engineering-faculty",
    "https://ai.meng.duke.edu/news/dukes-new-masters-degree-applies-ai-product-innovation",
    "https://ai.meng.duke.edu/news/shining-spotlight-diarra-bell",
    "https://ai.meng.duke.edu/news/shining-spotlight-eduardo-martinez",
    "https://ai.meng.duke.edu/news/shining-spotlight-shyamal-anadkat22",
    "https://ai.meng.duke.edu/news/using-ai-teach-ai-dukes-master-engineering-degree-program",
    "https://ai.meng.duke.edu/news/where-are-stem-jobs-north-carolinas-charlotte-no-1-and-raleigh-no-5-new-index",
    "https://ai.meng.duke.edu/why-duke",
    "https://ai.meng.duke.edu/why-duke/career-services",
    "https://ai.meng.duke.edu/why-duke/graduate-outcomes",
    "https://ai.meng.duke.edu/why-duke/tech-leaders"
]

# Create directories if not exist
if not os.path.exists('Data'):
    os.makedirs('Data')
if not os.path.exists('Data/scraped_html'):
    os.makedirs('Data/scraped_html')
if not os.path.exists('Data/scraped_text'):
    os.makedirs('Data/scraped_text')

# Open the combined_data.txt file in write mode
with open('Data/combined_data.txt', 'w') as combined_file:
    # Loop through each URL
    for url in urls:
        # Send a GET request
        response = requests.get(url)
        # Get the content of the response
        content = response.content
        # Create a BeautifulSoup object and specify the parser
        soup = BeautifulSoup(content, 'html.parser')

        # Save the HTML content
        with open(f'Data/scraped_html/{url.replace("http://", "")}.html', 'w') as html_file:
            html_file.write(soup.prettify())

        # Extract text from the BeautifulSoup object
        text = soup.get_text()

        # Save the text content
        with open(f'Data/scraped_text/{url.replace("http://", "")}.txt', 'w') as text_file:
            text_file.write(text)

        # Write the text content to the combined_data.txt file
        combined_file.write(text)
        combined_file.write('\n\n')  # add a couple of newlines between sites
