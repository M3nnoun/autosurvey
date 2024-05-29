import os
from dotenv import load_dotenv
import DataCollector as dc
## url form
url = "https://api.fillout.com/v1/api/forms/owxwseT6C3us/submissions"
# Define your API key
load_dotenv(dotenv_path='./.env')
api_key = os.getenv('API_KEY')
if not api_key:
    raise Exception("API_KEY environment variable not set")

fillout=dc.Fillout(url,api_key)

fillout.import_data()
print(fillout.export_data("me.csv"))
sheet_id = '1vZ4JaeJmq123eW62bE6H0YBd_J-1eJbhI0ar4jXUVWw'
google_sheet=dc.Sheet(sheet_id)

google_sheet.import_data("Sheet1")

google_sheet.export_data("data.csv")