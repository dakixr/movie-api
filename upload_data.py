import requests

url = "http://127.0.0.1:8000/load-data"

files_to_upload = [
    "test_data/IMDBMovies2000-2020.csv",
    "test_data/IMDBMovies2000-2020.xlsx"
]

for file_path in files_to_upload:
    with open(file_path, 'rb') as file:
        files = {'file': file}
        response = requests.post(url, files=files)
        print(f"Uploaded {file_path}: {response.status_code} - {response.text}")
