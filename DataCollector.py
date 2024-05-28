import requests
import json
import csv
class Collector:
    def __init__(self) -> None:
        pass
    
    def import_data(self):
        pass

    def export_data(self):
        print(self.name)
## handel data sources --> Fillout application
class Fillout(Collector):
    def __init__(self,url,api_key) -> None:
        super().__init__()
        self.url=url
        self.api=api_key
        self.current_data=None
    def import_data(self):
        headers = {
            "Authorization": f"Bearer {self.api}",
            "Content-Type": "application/json"
        }
        response = requests.get(self.url, headers=headers)
        if response.status_code == 200:
            response_content = response.content.decode('utf-8')
            data = json.loads(response_content)
            self.current_data=data
        else:
            error_message = f"Request failed with status code {response.status_code}\n{response.text}"
            raise Exception(error_message)

    def export_data(self,file_name) -> bool:
        
        if self.current_data is None:
            raise Exception("No data to export; please run import_data function before.")
        
        # get file formate
        file_format=file_name.split('.')[1].upper()
        if file_format=='JSON':
            with open(file_name, 'w',encoding='utf-8') as json_file:
                json.dump(self.current_data, json_file, ensure_ascii=False, indent=4)
                print(f"JSON response saved to {file_name}")
                return True
        if file_format=='CSV':
            #Prepare data == converting from json to dic {quetion:value}
            column_headers = ["submissionId", "submissionTime", "lastUpdatedAt"] + [q["name"] for q in self.current_data["responses"][0]["questions"]]
            csv_data = []
            for row in self.current_data['responses']:
                row_values = [row["submissionId"], row["submissionTime"], row["lastUpdatedAt"]] + [q["value"][0] if isinstance(q["value"], list) else q["value"]  for q in row["questions"]]
                csv_data.append(dict(zip(column_headers, row_values)))
            # Write to CSV file
            try:
                with open(file_name, 'w', encoding='utf-8', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=column_headers)
                    writer.writeheader()
                    writer.writerows(csv_data)
                print(f"Data saved to {file_name}")
                return True
            except IOError:
                raise Exception("I/O error")