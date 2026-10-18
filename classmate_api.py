
import requests

url = "https://flask-malunes-act4.onrender.com/campus"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    print("Classmate Campus Information")
    print("Campus:", data["campus"])
    print("Location:", data["location"])
    print("Type:", data["type"])
    print("Status:", data["status"])

else:
    print("Request failed.")
    print("Status Code:", response.status_code)
    print(response.text)
