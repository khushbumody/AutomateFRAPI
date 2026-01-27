import allure
import pytest

from aadhar_validation_api import call_aadhar_validation_api
from test_login_token1 import create_token

valid_aadhar = "NDgyNTM0MzA1MTA4"
invalid_aadhar = "123456789012"


# =====================================================
# TC1: Valid Aadhaar + Valid Token
# =====================================================
#
@all
@allure.title("TC1: Validate Aadhaar with valid token")
@allure.description("Validate Aadhaar number with valid token should return 200")
@pytest.mark.smoke
def test_valid_aadhar():
    token = create_token()
    response = call_aadhar_validation_api(token, valid_aadhar)
    assert response.status_code == 200, "Expected status code 200 for valid Aadhaar"
