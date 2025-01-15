import requests
from bs4 import BeautifulSoup


# Function to extract data from a single page
def extract_data_from_page(url):
    print(f"Fetching data from: {url}")  # Debugging log to show the page being fetched
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch {url} with status code {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all rows in the table (skip header row)
    rows = soup.find_all('tr')

    banks_info = []
    for row in rows:
        cells = row.find_all('td')

        # Ensure there are enough cells in the row
        if len(cells) >= 5:
            bank_name = cells[1].get_text(strip=True)
            city = cells[2].get_text(strip=True)
            swift_code = cells[4].find('a').get_text(strip=True)

            banks_info.append({
                "Bank Name": bank_name,
                "City": city,
                "SWIFT Code": swift_code
            })

    return banks_info


# Function to get the total number of pages from the first page
def get_total_pages(base_url):
    print(f"Fetching pagination information from: {base_url}")  # Debugging log
    response = requests.get(base_url)

    if response.status_code != 200:
        print(f"Failed to fetch pagination info from {base_url} with status code {response.status_code}")
        return 1  # Return 1 if the pagination can't be fetched

    soup = BeautifulSoup(response.content, 'html.parser')
    page_links = soup.find_all('span', class_='page-link')

    # Extract the last page number (it's in the last <a> tag)
    if page_links:
        last_page = page_links[-1].find('a')
        if last_page:
            return int(last_page.get_text())
    return 1  # Default to 1 if no pages are found


# Base URL of the website
base_url = "https://www.theswiftcodes.com/nigeria/"

# Get the total number of pages
total_pages = get_total_pages(base_url)

print(f"Total number of pages: {total_pages}")  # Debugging log

# Loop through each page and extract the data
all_banks_info = []
for page in range(1, total_pages + 1):
    url = f"{base_url}page/{page}/"  # Construct the full URL with page number
    banks_info = extract_data_from_page(url)
    all_banks_info.extend(banks_info)

# Print the extracted data
if all_banks_info:
    for bank in all_banks_info:
        print(f"Bank Name: {bank['Bank Name']}")
        print(f"City: {bank['City']}")
        print(f"SWIFT Code: {bank['SWIFT Code']}")
        print("-" * 40)
else:
    print("No data was extracted.")
