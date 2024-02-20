import requests
import base64
import json
from bs4 import BeautifulSoup

# Function to read data from config.json
def read_config(file_path):
    with open(file_path, 'r') as file:
        config_data = json.load(file)
    return config_data

# Function to update config.json with changed values
def update_config_data(file_path, changed_values):
    config_data = read_config(file_path)
    config_data.update(changed_values)
    with open(file_path, 'w') as file:
        json.dump(config_data, file, indent=4)

# Function to write data to trigger.json
def write_trigger_data(data):
    with open('trigger.json', 'w') as file:
        json.dump(data, file, indent=4)

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
        # Extracting table content from the page
        table_content = page_info['body']['storage']['value']
        
        # Using BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(table_content, 'html.parser')
        
        # Finding the starting point of the desired table
        start_tag = soup.find('p', string=lambda x: x and 'PROD - Openshift Deployments' in x)
        if start_tag:
            # Finding the next table sibling of the starting point
            table = start_tag.find_next_sibling('table')
            if table:
                # Initialize an empty dictionary to store application names and versions
                app_dict = {}

                # Find all rows in the table
                rows = table.find_all('tr')

                # Extract header row to determine column indexes
                header_row = rows[0]
                headers = [header.get_text(strip=True) for header in header_row.find_all(['th', 'td'])]

                # Find indexes of 'application name' and 'application version' columns
                app_name_index = headers.index('application name')
                app_version_index = headers.index('application version')

                # Loop through rows and extract application name and version
                for row in rows[1:]:
                    columns = row.find_all(['th', 'td'])
                    app_name = columns[app_name_index].get_text(strip=True)
                    app_version = columns[app_version_index].get_text(strip=True)
                    app_dict[app_name] = app_version

                # Print the dictionary
                print("Dictionary from HTML table:")
                print(app_dict)

                # Initialize a dictionary to store changed values
                changed_values = {}

                # Read data from config.json
                config_data = read_config('config.json')

                # Compare data from HTML table with data from config.json
                for key, value in app_dict.items():
                    if key in config_data:
                        if config_data[key] != value:
                            changed_values[key] = value

                # Print the changed values
                print("Changed values:")
                print(changed_values)

                # Write changed values to trigger.json
                write_trigger_data(changed_values)

                # Update config.json with changed values
                update_config_data('config.json', changed_values)
            else:
                print("No table found after 'PROD - Openshift Deployments'.")
        else:
            print("No starting point 'PROD - Openshift Deployments' found in the page.")
    else:
        print("No table content found on the page.")
else:
    # Print an error message if the request was not successful
    print(f"Error: {response.status_code} - {response.text}")
