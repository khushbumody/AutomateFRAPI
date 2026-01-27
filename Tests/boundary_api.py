# boundary_api.py
import allure
import requests


@allure.feature("Boundary API")
@allure.story("Fetch Accessible Boundary List")
def call_boundary_api(token):
    url = (
        "https://trngfr.agristack.gov.in/"
        "farmer-registry-api-training-as/agristack/v1/api/user/getAccessibleBoundaryByList"
    )

    headers = {
        "accept": "application/json, text/plain, */*",
        "authorization": f"Bearer {token}",
        "content-type": "application/json",
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

    body = {"boundaryType": "state"}

    response = requests.post(url, headers=headers, json=body)

    allure.attach(str(body), "Request Body", allure.attachment_type.JSON)
    allure.attach(response.text, "Boundary API Response", allure.attachment_type.JSON)

    return response


# Manual debug
if __name__ == "__main__":
    print("Run tests instead.")
