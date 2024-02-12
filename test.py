import requests
from bs4 import BeautifulSoup
import base64

# Replace these values with your Confluence site URL, page ID, and base64-encoded token
confluence_url = "https://sharmasid2398.atlassian.net/wiki"
page_id = "163997"
base64_encoded_token = "c2hhcm1hc2lkMjM5OEBnbWFpbC5jb206QVRBVFQzeEZmR0YwaHdEbVBXTmFGT184WTJKYkNJajFYbDE2LTlIZUdaR21kdTQxRFVYNURmRGdZY1QxMW5GMUhOekpjUjh1bkRsRWlfMFh0R0ctZTZsd1JXWDZZR0xOckdSbHV2SWpCTFJySlVjdUJwX3VJMnM5VVhVX3oyN3VzSFBNS0RaOVZGVUtuYXpEMWtybUQzVlIxbHJmb3ExeXJSaDNKQ1hrMWJUYlhKSkRrUDh5dkJZPTY0QjA4NzUw"

# Construct the API endpoint URL
api_url = f"{confluence_url}/rest/api/content/{page_id}?expand=body.storage"

# Set up headers with the base64-encoded token
headers = {
    "Authorization": f"Basic {base64_encoded_token}",
    "Content-Type": "application/json",
}

# Make a GET request to the Confluence API
response = requests.get(api_url, headers=headers)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response
    page_info = response.json()

    # Extract and print the table content if present
    if 'body' in page_info and 'storage' in page_info['body'] and 'value' in page_info['body']['storage']:
        table_content = page_info['body']['storage']['value']

        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(table_content, 'html.parser')
        
        # Find all rows in the table
        rows = soup.find_all('tr')

        # Skip the first row (header) and loop through the remaining rows to print cell data
        for row in rows[1:]:
            columns = row.find_all(['th', 'td'])
            for column in columns:
                print(column.get_text(strip=True), end='\t')
            print()  # Move to the next line for the next row

    else:
        print("No table content found on the page.")

else:
    # Print an error message if the request was not successful
    print(f"Error: {response.status_code} - {response.text}")
