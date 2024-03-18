import requests
from bs4 import BeautifulSoup

def scrape_website_to_markdown(url, output_file):
    # Send an HTTP GET request to the website
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Open a file to write the Markdown content
        with open(output_file, 'w', encoding='utf-8') as file:
            # Find the elements that contain the data you're interested in
            # For example, to output paragraphs as Markdown, you might do:
            paragraphs = soup.find_all('p')
            for paragraph in paragraphs:
                # Write each paragraph to the file formatted as Markdown
                # For simplicity, we just write the text. Markdown adjustments can be added as needed.
                file.write(f"{paragraph.text}\n\n")
                
            # You can add more code here to handle other elements (e.g., headers, lists) and format them accordingly

# This function call is purely hypothetical and should not be used without permission
scrape_website_to_markdown('https://www.nav.no/ukraina', 'output.md')
