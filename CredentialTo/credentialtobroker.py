"""CredentialToBroker.py: This module contains credential classes for various brokers."""


class CredentialFinvasia:
    """Shoonya Finvasia API Credentials"""

    VendorCode = "FN175412_U"
    IMEI = "abc1234"
    APIKEY = "87bd0e9ba9fbe83ec81f85caaa4d86fc"
    Uid = "FN175412"
    Password = "Rohitd@84"


class CredentialFyers:
    """Fyers API Credentials"""

    client_id = ''  # Client_id here refers to APP_ID of the created app
    secret_key = ''  # app_secret key which you got after creating the app
    # redircet_uri you entered while creating APP.
    redirect_uri = ''
    # The grant_type always has to be "authorization_code"
    response_type = "code"  # The response_type always has to be "code"
    state = "sample"  # The state field here acts as a session manager.
    grant_type = "authorization_code"
