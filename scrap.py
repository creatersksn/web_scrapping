import requests
from bs4 import BeautifulSoup
import csv
import time

# Specify the URL of the website you want to scrape
url = 'https://anar.biz/directory/retailers'

# Create lists to store the data
data_list = []

# Counter to keep track of the number of records collected
record_count = 0

# Send an HTTP GET request to the URL after waiting for a few seconds
time.sleep(5)
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all elements with class "w-full"
    elements_with_w_full_class = soup.find_all(class_="grid grid-cols-1 lg:grid-cols-3 w-full gap-y-3 gap-x-20")

    # Loop through the elements with the "w-full" class
    for element in elements_with_w_full_class:
        # Find all links (anchor tags) within each element
        links = element.find_all('a')

        # Loop through the links
        for link in links:
            # Get the href attribute of the link
            link_url = link.get('href')

            # Send an HTTP GET request to the link URL after waiting for a few seconds
            time.sleep(2)
            link_response = requests.get("https://anar.biz/"+link_url)

            # Check if the request was successful
            if link_response.status_code == 200:
                # Parse the HTML content of the linked page
                linked_soup = BeautifulSoup(link_response.text, 'html.parser')

                # Find the text within the first <h1> tag on the linked page
                h1_tag = linked_soup.find('h1')
                h1_text = h1_tag.text if h1_tag else ''

                # Find the text within elements with the class "text-xs lg:text-sm text-grey600 leading-2"
                text_elements = linked_soup.find_all(class_="text-xs lg:text-sm text-grey600 leading-2")
                text_elements_text = [text_element.text for text_element in text_elements]

                # Find the text within elements with the class "text-sm text-black"
                black_text_elements = linked_soup.find_all(class_="text-sm text-black")
                black_text_elements_text = [black_text_element.text for black_text_element in black_text_elements]

                # Append the data to the data_list
                data_list.append([h1_text] + text_elements_text + black_text_elements_text)

                # Increment the record count
                record_count += 1
                print(record_count)
            else:
                print(f'Failed to retrieve {link_url}. Skipping to the next URL.')
else:
    print('Failed to retrieve the webpage.')

# Define the CSV filename
csv_filename = 'scraped_data.csv'

# Write the data to a CSV file
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)

    # Write the header row
    header = ["H1 Text", "Text Elements", "Black Text Elements"]
    csv_writer.writerow(header)

    # Write the data rows
    csv_writer.writerows(data_list)

print(f'Data has been exported to {csv_filename}.')
print(f'Collected {record_count} records.')
