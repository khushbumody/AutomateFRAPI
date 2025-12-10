import requests
import allure


@allure.feature("Token Generation")
@allure.story("Create Token for Authorization")
def create_token():
    url = "https://trngfr.agristack.gov.in/farmer-registry-api-training-as/agristack/v1/api/authenticate/user/loginUserOtpValidate"
    headers = {"accept": "application/json, text/plain, */*"}
    payload = "e2ar3Pg10SMnGvH18IfCcHa1H8r0q+Zmb6GDmm5u82BwYzBA2oIAZ7Cg+n9yAJy73eSuF5Hjcfl0QnMIuurhNTZwvqBafKkL8GWvE0UvR7xLekgPN/Hh31tzG4NeS76P"

    response = requests.post(url, headers=headers, data=payload)
    print("API Response:", response.text)

    assert response.status_code == 200

    token = None
    try:
        token = response.json().get("token")
    except ValueError:
        # response not JSON — leave token as None
        pass

    return token


def test_create_token():
    """pytest test: call create_token and assert a token is returned"""
    token = create_token()
    assert token is not None


if __name__ == "__main__":
    # allow running directly: python Tests/test_login_token.py
    t = create_token()
    print("Returned token:", t)
