import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
from bs4 import BeautifulSoup


def authenticate_google_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    return client.open("swift codes extractor")


def extract_data_from_page(url):
    print(f"Fetching data from: {url}")
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch {url} with status code {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    rows = soup.find_all('tr')

    banks_info = []
    for row in rows:
        cells = row.find_all('td')

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


def get_total_pages(base_url):
    print(f"Fetching pagination information from: {base_url}")
    response = requests.get(base_url)

    if response.status_code != 200:
        print(f"Failed to fetch pagination info from {base_url} with status code {response.status_code}")
        return 1

    soup = BeautifulSoup(response.content, 'html.parser')
    page_links = soup.find_all('span', class_='page-link')

    if page_links:
        last_page = page_links[-1].find('a')
        if last_page:
            return int(last_page.get_text())
    return 1


base_url = "https://www.theswiftcodes.com/nigeria/"

total_pages = get_total_pages(base_url)

print(f"Total number of pages: {total_pages}")

all_banks_info = []
for page in range(1, total_pages + 1):
    if page == 1:
        url = base_url
    else:
        url = f"{base_url}page/{page}/"

    banks_info = extract_data_from_page(url)
    all_banks_info.extend(banks_info)

if all_banks_info:
    sheet = authenticate_google_sheet()
    worksheet = sheet.get_worksheet(0)

    headers = ["Bank Name", "City", "SWIFT Code"]

    # Use batch_update to write multiple rows at once
    cell_list = worksheet.range(f"A2:C{len(all_banks_info) + 1}")  # A2 is where data starts (A1 is for header)

    for i, bank in enumerate(all_banks_info):
        cell_list[i * 3].value = bank["Bank Name"]
        cell_list[i * 3 + 1].value = bank["City"]
        cell_list[i * 3 + 2].value = bank["SWIFT Code"]

    worksheet.update_cells(cell_list)  # Update all cells in the batch

    print("Data has been successfully added to the Google Sheet.")
else:
    print("No data was extracted.")
