# test_boundary_api.py
import allure
import pytest
from test_login_token1 import create_token
from boundary_api import call_boundary_api


@allure.title("Token pass ")
@allure.description("Create Token for Authorization")
@pytest.mark.smoke
def test_boundary_api_flow():
    """Full flow: create token -> use token in boundary API"""

    # Step 1: Generate token
    token = create_token()
    assert token is not None, "Token generation failed"

    # Step 2: Use token in boundary API
    response = call_boundary_api(token)

    assert response.status_code == 200, "Boundary API did not return 200 OK"

    json_data = response.json()
    assert "data" in json_data, "Boundary API response missing 'data' field"
