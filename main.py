import requests
from bs4 import BeautifulSoup

# Send a GET request to the URL
url = "https://www.theswiftcodes.com/nigeria/"
response = requests.get(url)

# Parse the content of the page with BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find all rows in the table (skip header row)
rows = soup.find_all('tr')

# Loop through the rows and extract the bank name, city, and swift code
banks_info = []
for row in rows:
    cells = row.find_all('td')

    if len(cells) >= 5:  # Ensure there are enough cells in the row
        bank_name = cells[1].get_text(strip=True)
        city = cells[2].get_text(strip=True)
        swift_code = cells[4].find('a').get_text(strip=True)

        banks_info.append({
            "Bank Name": bank_name,
            "City": city,
            "SWIFT Code": swift_code
        })

# Print the extracted data
for bank in banks_info:
    print(f"Bank Name: {bank['Bank Name']}")
    print(f"City: {bank['City']}")
    print(f"SWIFT Code: {bank['SWIFT Code']}")
    print("-" * 40)
