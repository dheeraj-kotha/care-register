import requests

url = "https://www.register2park.com/register"

form_data = {
    "aptNumber": "1365",                     # Your apartment number
    "make": "bwm",                        # Your car make
    "model": "360i",                        # Your car model
    "licensePlate": "RBV6983",                # License plate
    "confirmLicensePlate": "RBV6983",         # Confirm plate
    "key": "4wddrlcphom8"                    # Location key from URL
}

response = requests.post(url, data=form_data)

if response.status_code == 200 and "Thank you for registering" in response.text:
    print("✅ Successfully submitted form!")
else:
    print(f"❌ Submission may have failed. Status code: {response.status_code}")
    print(response.text)  # For debugging
