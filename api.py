import requests

url = "https://daily-petrol-diesel-lpg-cng-fuel-prices-in-india.p.rapidapi.com/v1/fuel-prices/today/india/telangana"

headers = {
	"x-rapidapi-key": "9e7ffde3femsh7b97028a7f75e86p1af75djsn1261d0f865bc",
	"x-rapidapi-host": "daily-petrol-diesel-lpg-cng-fuel-prices-in-india.p.rapidapi.com"
}

response = requests.get(url, headers=headers)

print(response.json())