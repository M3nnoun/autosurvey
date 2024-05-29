import requests
import json
import csv
import pandas as pd
class Collector:
    def __init__(self) -> None:
        pass
    
    def import_data(self):
        """Method to be overridden in subclasses to import data."""
        pass

    def export_data(self, file_name: str) -> bool:
        """Method to be overridden in subclasses to export data."""
        raise NotImplementedError("Subclasses should implement this method")

class Fillout(Collector):
    def __init__(self, url: str, api_key: str) -> None:
        super().__init__()
        self.url = url
        self.api_key = api_key
        self.current_data = None

    def import_data(self) -> None:
        """Fetches data from the API and stores it in the current_data attribute."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        response = requests.get(self.url, headers=headers)
        if response.status_code == 200:
            self.current_data = response.json()
        else:
            error_message = f"Request failed with status code {response.status_code}\n{response.text}"
            raise Exception(error_message)

    def export_data(self, file_name: str) -> bool:
        """Exports the data to a file in either JSON or CSV format."""
        if self.current_data is None:
            raise Exception("No data to export; please run import_data function before.")
        
        file_format = file_name.split('.')[-1].upper()
        if file_format == 'JSON':
            return self._export_to_json(file_name)
        elif file_format == 'CSV':
            return self._export_to_csv(file_name)
        else:
            raise ValueError("Unsupported file format. Use 'json' or 'csv'.")

    def _export_to_json(self, file_name: str) -> bool:
        with open(file_name, 'w', encoding='utf-8') as json_file:
            json.dump(self.current_data, json_file, ensure_ascii=False, indent=4)
            print(f"JSON response saved to {file_name}")
        return True

    def _export_to_csv(self, file_name: str) -> bool:
        column_headers = ["submissionId", "submissionTime", "lastUpdatedAt"] + [q["name"] for q in self.current_data["responses"][0]["questions"]]
        csv_data = []
        for row in self.current_data['responses']:
            row_values = [row["submissionId"], row["submissionTime"], row["lastUpdatedAt"]] + [q["value"][0] if isinstance(q["value"], list) else q["value"] for q in row["questions"]]
            csv_data.append(dict(zip(column_headers, row_values)))

        try:
            with open(file_name, 'w', encoding='utf-8', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=column_headers)
                writer.writeheader()
                writer.writerows(csv_data)
            print(f"Data saved to {file_name}")
            return True
        except IOError as e:
            raise Exception(f"I/O error: {e}")

## create a google sheet data collector
## make a request using pandas for this url:
## https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}

class Sheet(Collector):
    def __init__(self,sheet_id) -> None:
        super().__init__()
        self.sheet_id=sheet_id
        self.current_data=None
    def import_data(self,sheet_name) -> bool:
        url = f'https://docs.google.com/spreadsheets/d/{self.sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
        try:
            df = pd.read_csv(url)
            if df is not None:
                self.current_data = df
                return True
            else:
                return False
        except Exception as e:
            raise e

    def export_data(self, file_name: str) -> bool:
        """Exports the data to a file in either JSON or CSV format."""
        if self.current_data is None:
            raise Exception("No data to export; please run import_data function before.")
        
        file_format = file_name.split('.')[-1].upper()
        if file_format == 'JSON':
            try:
                self.current_data.to_csv(file_name)
                return True
            except Exception as e:
                return False

        elif file_format == 'CSV':
            try:
                self.current_data.to_csv(file_name)
                return True
            except Exception as e:
                return False
        else:
            raise ValueError("Unsupported file format. Use 'json' or 'csv'.")        
