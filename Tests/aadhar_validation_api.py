# aadhar_validation_api.py
import allure
import requests


@allure.feature("Aadhaar Validation API")
@allure.story("Validate Aadhaar Number")
def call_aadhar_validation_api(token, aadhaar_number):


    url = (
        "https://trngfr.agristack.gov.in/"
        "farmer-registry-api-training-as/agristack/v1/api/"
        f"admin/general/validateAadhaarNumber?aadhaarNumber={aadhaar_number}"
    )

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "authorization": f"Bearer {token}",
        "origin": "https://trngfr.agristack.gov.in",
        "referer": "https://trngfr.agristack.gov.in/farmer-registry-training-as-ui/",
        "sec-ch-ua": '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
        ),
    }

    response = requests.get(url, headers=headers)

    allure.attach(url, "Request URL", allure.attachment_type.TEXT)
    allure.attach(response.text, "Aadhaar API Response", allure.attachment_type.JSON)

    return response
