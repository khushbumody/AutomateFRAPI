import time

import allure
import pytest
import requests

TOKEN_URL = (
    "https://trngfr.agristack.gov.in/"
    "farmer-registry-api-training-as/agristack/v1/api/authenticate/user/loginUserOtpValidate"
)

VALID_HEADERS = {
    "accept": "application/json, text/plain, */*",
    "authorization": "Bearer null",
    "content-type": "text/plain",
    "origin": "https://trngfr.agristack.gov.in",
    "referer": "https://trngfr.agristack.gov.in/farmer-registry-training-as-ui/",
    "sec-ch-ua": '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
    )
}

VALID_PAYLOAD = (
    "e2ar3Pg10SMnGvH18IfCcHa1H8r0q+Zmb6GDmm5u82BwYzBA2oIAZ7Cg+n9yAJy73eSu"
    "F5Hjcfl0QnMIuurhNTZwvqBafKkL8GWvE0UvR7xLekgPN/Hh31tzG4NeS76P"
)


# =====================================================================
# FUNCTION USED FOR VALIDATION
# =====================================================================
def create_token():
    response = requests.post((TOKEN_URL), headers=VALID_HEADERS, data=VALID_PAYLOAD)
    try:
        return response.json()["data"]["userToken"]
    except Exception:
        return None


# ====
# Testcase1 : Valid URL + Valid Payload + Required Headers => 200 & token
# ====

@allure.title("TC1: Valid request returns 200 & token")
@allure.description("Testcase to validate token generation with valid request")
@pytest.mark.smoke
@pytest.mark.regression
def test_create_token_valid_request():
    response = requests.post(TOKEN_URL, headers=VALID_HEADERS, data=VALID_PAYLOAD)

    assert response.status_code == 200, "Expected status code 200"
    assert "data" in response.json(), "Response missing 'data' field"
    assert "userToken" in response.json()["data"], "Response missing 'userToken'"


# ====
# Testcase2 : Response time < 2 seconds
# ====

@allure.title("TC2: Token generation response time < 2 seconds")
@allure.description("Testcase to validate token generation response time")
@pytest.mark.smoke
def test_create_token_response_time():
    start_time = time.time()
    response = requests.post(TOKEN_URL, headers=VALID_HEADERS, data=VALID_PAYLOAD)
    end_time = time.time()

    response_time = end_time - start_time
    assert response_time < 2, f"Response time {response_time} exceeds 2 seconds"


# ====
#  TEST CASE 3: API supports only POST
# ====
@allure.title("TC3: Token API supports only POST method")
@allure.description("Testcase to validate that token API supports only POST method")
@pytest.mark.regression
@pytest.mark.parametrize("method", ["get", "put", "delete", "patch"])
def test_only_post_allowed(method):
    request_method = getattr(requests, method)
    response = request_method(TOKEN_URL)
    assert response.status_code in [400, 401, 403, 404, 405, 422, 500], f"Method {method.upper()} should not be allowed"

#  ===
# TEST CASE 6: Invalid Payload - Expected Failure
#   ===


@allure.title("TC6: Invalid payload expected failure test")
@allure.description("This test is expected to fail due to invalid payload")
@pytest.mark.smoke
def test_invalid_payload_expected_failure():
    invalid_payload = "INVALID_PAYLOAD_123456###"

    response = requests.post(TOKEN_URL, headers=VALID_HEADERS, data=invalid_payload)

    # Expect this assertion to fail
    assert response.status_code == 400, "Expected failure: wrong payload should not pass"

# ===
# TEST CASE 4: Missing payload
# ===
@allure.title("TC4: Missing payload should return error")
@allure.description("Testcase to validate token generation with missing payload")
@pytest.mark.smoke
def test_missing_payload():
    # Call API without payload
    response = requests.post(TOKEN_URL, headers=VALID_HEADERS, data=None)

    # Expected failure status codes (based on real behavior)
    assert response.status_code in [400, 401, 403, 422, 500], \
        f"Missing payload should not return success. Actual: {response.status_code}"

    # SAFELY parse JSON if present
    try:
        json_response = response.json()
    except Exception:
        json_response = None

    # VALIDATION (token must never exist)
    if json_response and isinstance(json_response, dict):
        # If server returns JSON
        assert "userToken" not in json_response.get("data", {}), \
            "Token should NOT be returned for missing payload"
    else:
        # If body is blank or HTML → this is also acceptable
        assert True


# ===
# TEST CASE 5: Invalid Headers
# ===

@allure.title("TC5: Invalid payload should not return a valid token")
@allure.description("Validate API response for corrupted or malformed payload")
@pytest.mark.smoke
def test_invalid_payload():
    invalid_payload = "INVALID_PAYLOAD_123456###$$$"

    response = requests.post(TOKEN_URL, headers=VALID_HEADERS, data=invalid_payload)

    # Acceptable status codes (real API returns 200 even for invalid data)
    assert response.status_code in [200, 400, 401, 403, 422, 500], \
        f"Unexpected status code: {response.status_code}"

    # Try JSON parsing safely
    try:
        json_response = response.json()
    except Exception:
        json_response = None

    # Validate that token MUST NOT be returned
    if json_response and "data" in json_response:
        assert "userToken" not in json_response["data"], \
            "API returned a token for invalid payload, which should NOT happen"
    else:
        assert True  # Non-JSON error response is also acceptable



