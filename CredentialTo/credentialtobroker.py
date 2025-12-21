"""CredentialToBroker.py: This module contains credential classes for various brokers."""


class CredentialFinvasia:
    """Shoonya Finvasia API Credentials"""

    VendorCode = "DDIPS7674J_U"
    IMEI = "abc1234"
    APIKEY = "96c9f687f6b479139965247a79bfb738"
    Uid = "DDIPS7674J"
    Password = "Rohitd84"


class CredentialFyers:
    """Fyers API Credentials"""

    client_id = 'JY54W40EMC-100'  # Client_id here refers to APP_ID of the created app
    secret_key = 'A7IMMK20VJ'  # app_secret key which you got after creating the app
    # redircet_uri you entered while creating APP.
    redirect_uri = 'https://www.google.com/'
    # The grant_type always has to be "authorization_code"
    response_type = "code"  # The response_type always has to be "code"
    state = "sample"  # The state field here acts as a session manager.
    grant_type = "authorization_code"
