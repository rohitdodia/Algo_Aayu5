from BrokerAPI.kiteconnectAPI import ShoonyaApiPy
from CredentialTo.CredentialToBroker import CredentialKiteconnect


class InterfaceFinvasia:
    # 1. Function to initialize the Finvasia interface
    def __init__(self):
        print("Connecting to Finvasia Broker API...")
        # process initialization here
        self._shoonyAPi = ShoonyaApiPy()  # acting as private member

    # 2. Function to display login panel
    def login_panel(self):
        # 6 digit code from 2FA app as per broker requirement
        totp = self._get_totp_factor()

        if totp == -1:
            print("Login aborted due to TOTP generation error..")
            return

        # Implement login panel logic here
        # Converting totp factor from int to string for better readability
        totp = str(totp)
        ret = self._shoonyAPi.login(userid=CredentialFinvasia.Uid,
                                    password=CredentialFinvasia.Password,
                                    twoFA=totp,
                                    vendor_code=CredentialFinvasia.VendorCode,
                                    api_secret=CredentialFinvasia.APIKEY,
                                    imei=CredentialFinvasia.IMEI)
        print(F"Broker Replied: {ret} ")

    # 3. Function to get TOTP factor for 2FA
    def _get_totp_factor(self):  # private method to get TOTP factor
        try:  # try block to handle exceptions
            print("Please Enter TOTP (6 digit) Numeric Character")  # prompt user
            result = int(input())  # get user input and CPU wait for user input
            return result  # return the entered TOTP

        except Exception as e:  # handle exception
            print(F"Error in generating TOTP factor: str(e)")  # log error
            return -1  # indicate failure
