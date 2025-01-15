# Swift Codes Extractor

This Python script extracts bank names, cities, and SWIFT codes from the website [The Swift Codes - Nigeria](https://www.theswiftcodes.com/nigeria/) and stores the extracted data into a Google Sheet.

## How It Works

1. **Scraping Data**: The script scrapes data from multiple pages on the website and collects:
   - Bank Name
   - City
   - SWIFT Code

2. **Pagination Handling**: The script automatically handles pagination, fetching all pages of data.

3. **Saving to Google Sheets**: The extracted data is saved into a Google Sheet using the Google Sheets API.

## Setup

### Google Sheets API Credentials

1. Go to the [Google Developers Console](https://console.developers.google.com/).
2. Create a new project or select an existing one.
3. Enable the **Google Sheets API** and **Google Drive API** for your project.
4. Create **Service Account Credentials** and download the `credentials.json` file.
5. Place the `credentials.json` file in the root of your project directory (where this script is located).

### Google Sheet

1. Create a new Google Sheet named **swift codes extractor**.
2. Share the sheet with the email address associated with the service account (you'll find this in the `credentials.json` file).
3. Ensure the Google Sheet is accessible to the service account.

## Usage

1. Place the `credentials.json` file in the root directory of the project (the same directory as this script).
2. Run the script:

```bash
python swift_codes_extractor.py
```
