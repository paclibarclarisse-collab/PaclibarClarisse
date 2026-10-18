
import requests

url = "https://paclibarclarisse.onrender.com/subjects"

response = requests.get(url)

print("Status Code:", response.status_code)

if response.status_code == 200:
    data = response.json()

    print("Student:", data["student"])
    print("Subjects:")

    for subject in data["subjects"]:
        print("-", subject)

    print("Semester:", data["semester"])
else:
    print(response.text)
