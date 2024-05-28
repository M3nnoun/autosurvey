import os
from dotenv import load_dotenv
import DataCollector as dc
## url form
url = "https://api.fillout.com/v1/api/forms/owxwseT6C3us/submissions"
# Define your API key
api_key = os.getenv('API_KEY')
if not api_key:
    raise Exception("API_KEY environment variable not set")

fillout=dc.Fillout(url,api_key)

fillout.import_data()
print(fillout.export_data("me.csv"))