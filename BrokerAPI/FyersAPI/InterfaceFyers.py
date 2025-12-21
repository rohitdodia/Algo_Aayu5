from BrokerAPI.FyersAPI.fyers_apiv3.fyers_logger import FyersLogger
from BrokerAPI.FyersAPI.fyers_apiv3.fyersModel import fyersModel
import webbrowser
from CredentialTo.CredentialToBroker import CredentialFyers


class InterfaceFinvasia:
    # 1. Function to initialize the Finvasia interface
    def __init__(self):
        print("Connecting to Finvasia Broker API...")
        # process initialization here
        self._fyersModelAPI = fyersModel()  # acting as private member

        self._isconnected = False  # connection status flag

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
        ret = self._fyersModelAPI.login(redirect_uri=CredentialFyers.redirect_uri,
                                        client_id=CredentialFyers.client_id,
                                        secret_key=CredentialFyers.secret_key,
                                        grant_type=CredentialFyers.grant_type,
                                        response_type=CredentialFyers.response_type,
                                        state=CredentialFyers.state)
        print(F"Broker Replied: {ret} ")
        # Ok or Not OK
        print(F"Connection Establised to Broker : {ret['stat']}")

        if ret['stat'] == "Ok":
            print("Case 2 : Successfully Logged in to Fyers Broker API")
            self._sucessfully_connected()
        elif ret['state'] == "Not_Ok":
            print("Case 1 : Login Failed.")

    # 3. Function to get TOTP factor for 2FA
    def _get_totp_factor(self):  # private method to get TOTP factor
        try:  # try block to handle exceptions
            print("Please Enter TOTP (6 digit) Numeric Character")  # prompt user
            result = input()  # get user input and CPU wait for user input

            check_length_of_input = len(result)  # check length of input
            if check_length_of_input != 6:  # validate length
                print("Invalid TOTP Length. It should be 6 digits.")  # log error
                return self._get_totp_factor()  # recursive call to re-prompt
            result = int(result)  # convert input to integer

            return result  # return the entered TOTP

        except Exception as e:  # handle exception
            print(F"Error in generating TOTP factor: str(e)")  # log error
            return -1  # indicate failure

    # 4. Function Connection Establishment == "OK"
    def _sucessfully_connected(self):
        try:
            self._isconnected = True  # implement connection check logic here
        except Exception as e:
            print(F"Error in connection establishment: str(e)")

    # 5. Function to Confirm client about connection status {Ok, NOT OK}
    def IsConnected(self):  # this public method
        return self._isconnected  # False

    # 6. Function to Requseting Data from broker Server
    def RequestToBroker(self):

        if self.IsConnected() == False:  # check connection status
            print("Please Connect to broker server first.")
            return  # early return

    # 7. Function to close connection forecefully - Logout
    def CloseAPI(self):
        try:
            if self.IsConnected() == False:
                print("Already Disconnected from Broker API.")
                return

            result = self._fyersModelAPI.logout()  # call logout method from ShoonyaApiPy
            if result['stat'] == "Ok":
                print("Successfully logged out from Broker API.")
            else:
                print("Logout Failed from Broker API.")
        except Exception as e:
            print(F"Error in logging out: str(e)")
